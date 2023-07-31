# Generated by Django 4.2.3 on 2023-07-25 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_training', '0006_course_amount_payment_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='intent_id',
            field=models.CharField(default=1, max_length=100, verbose_name='ID платежного намерения'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(default='requires_payment_method', max_length=20, verbose_name='Статус'),
        ),
    ]