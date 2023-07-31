from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from online_training.models import Course, Lesson, Payment, Subscription
from online_training.pagination import CoursePagination, LessonPagination
from online_training.permissions import ModeratorPermission, OwnerPermission
from online_training.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer, \
    PaymentIntentCreateSerializer, PaymentMethodCreateSerializer, PaymentConfirmSerializer
from online_training.services import StripePayment
from .tasks import notify_course_updates


# ViewSets
class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ModeratorPermission | OwnerPermission]
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.groups.filter(name='Модератор').exists():
                return Course.objects.all()
            return Course.objects.filter(author=user)
        return Course.objects.none()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        self.object = serializer.save()
        notify_course_updates.delay(self.object.pk)


class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'paid_method']
    ordering_fields = ['date']

# Generics
class LessonListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,  ModeratorPermission | OwnerPermission]
    serializer_class = LessonSerializer
    pagination_class = LessonPagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Модератор').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(author=user)


class LessonCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,  ModeratorPermission | OwnerPermission]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, ModeratorPermission | OwnerPermission]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, OwnerPermission | ModeratorPermission]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, ModeratorPermission | OwnerPermission]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class SubscriptionListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

class SubscriptionDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

class SubscriptionCreateView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]

class SubscriptionDeleteView(generics.DestroyAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]

class SubscriptionUpdateView(generics.UpdateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]

class PaymentIntentCreateView(generics.GenericAPIView):
    serializer_class = PaymentIntentCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course_id = serializer.validated_data['course_id']
        user_id = request.user.id

        try:
            payment_intent = StripePayment.create_payment_intent(course=course_id, user=user_id)
            payment = get_object_or_404(Payment, intent_id=payment_intent['id'])
            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({'ERROR': str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class PaymentMethodCreateView(generics.GenericAPIView):
    serializer_class = PaymentMethodCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        intent_id = serializer.validated_data['intent_id']
        pay_token = serializer.validated_data['pay_token']

        try:
            StripePayment.match_payment_method(intent_id=intent_id, pay_token=pay_token)
            payment = get_object_or_404(Payment, intent_id=intent_id)
            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({'ERROR': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

class PaymentConfirmView(generics.GenericAPIView):
    serializer_class = PaymentConfirmSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        intent_id = serializer.validated_data['intent_id']

        try:
            StripePayment.confirm_payment(intent_id=intent_id)
            payment = get_object_or_404(Payment, intent_id=intent_id)
            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response({'ERROR': str(ex)}, status=status.HTTP_400_BAD_REQUEST)