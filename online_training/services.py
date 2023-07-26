import requests
from config import settings
from online_training.models import Payment
from online_training.models import Course
from user.models import User


class StripePayment:
    TOKEN = settings.PAYMENT_TOKEN

    @classmethod
    def create_payment_intent(cls, course, user):
        course = Course.objects.get(id=course)
        amount = int(course.amount)
        user = User.objects.get(id=user)

        data = {
            'amount': amount,
            'currency': 'rub',
            'automatic_payment_methods[enabled]': 'false',
            'metadata[course]': course,
            'metadata[user]': user,
        }
        response = requests.post('https://api.stripe.com/v1/payment_intents', data=data, auth=(cls.TOKEN, '')).json()

        Payment.objects.create(
            user=user,
            course=course,
            paid=amount,
            status=response['status'],
            intent_id = response['id']
        )

        return response

    @classmethod
    def create_payment_method(cls, pay_token):
        data = {
            'type': 'card',
            'card[token]': pay_token
        }
        response = requests.post('https://api.stripe.com/v1/payment_methods', data=data, auth=(cls.TOKEN, '')).json()

        return response

    @classmethod
    def match_payment_method(cls, intent_id, pay_token):
        payment_method = cls.create_payment_method(pay_token)
        data = {
            'payment_method': payment_method['id']
        }
        response = requests.post(f'https://api.stripe.com/v1/payment_intents/{intent_id}', data=data, auth=(cls.TOKEN, '')).json()
        payment = Payment.objects.get(intent_id=intent_id)
        payment.method_id = payment_method['id']
        payment.status = response['status']
        payment.save()

        return response


    @classmethod
    def confirm_payment(cls, intent_id):
        payment = Payment.objects.get(intent_id=intent_id)
        if payment.method_id:
            data = {'payment_method': payment.method_id}
            response = requests.post(
                f'https://api.stripe.com/v1/payment_intents/{intent_id}/confirm',
                data=data,
                auth=(cls.TOKEN, '')
            ).json()
        else:
            raise Exception('ERROR: Payment is not found')

        payment.status = response['status']
        payment.save()

        return response
