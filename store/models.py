from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ("0", "Created"),
        ("1", "Accepted"),
    )

    customer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='orders',
        verbose_name='Замовник',
        null=True,
    )
    status = models.CharField(
        max_length=40,
        verbose_name="Статус замовлення",
        choices=ORDER_STATUS_CHOICES,
        default="0",
    )

    def __str__(self) -> str:
        if self.customer is None:
            return f"Замовлення № {self.pk}"
        else:
            return f"Замовлення № {self.pk} від {self.customer}"
    
    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"