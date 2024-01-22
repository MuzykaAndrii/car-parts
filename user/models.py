from django.db import models
from django.contrib.auth.models import User


class ShippingAddress(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="shipping_address",
        verbose_name="Адреса доставки",
    )
    first_name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name="Імя",
    )
    last_name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name="Прізвище",
    )
    phone_number = models.CharField(
        max_length=15,
        null=False,
        blank=False,
        verbose_name="Номер телефону",
    )
    region = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name="Область",
    )
    city = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name="Населений пункт",
    )
    office_number = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name="Номер відділення",
    )
