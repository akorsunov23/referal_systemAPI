# Generated by Django 4.2.3 on 2023-08-02 06:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0003_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Номер телефона должен быть введен в формате: "81234567890". Максимальная длина 11 символов.', regex='^8\\d{10}$')], verbose_name='номер телефона'),
        ),
    ]
