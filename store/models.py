from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    class OrderStatus(models.IntegerChoices):
        GATHERING = 1, "В корзині"
        PROCESSING = 2, "Замовлення здійснено"
        IN_TRANSIT = 3, "У процесі доставки"
        IN_DESTINATION = 4, "Замовлення у поштовому відділенні"
        RECEIVED = 5, "Замовлення отримано"
        REFUSED = 6, "Замовлення повернено"


    customer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='orders',
        verbose_name='Замовник',
        null=True,
    )
    status = models.PositiveSmallIntegerField(
        verbose_name="Статус замовлення",
        choices=OrderStatus.choices,
        default=OrderStatus.GATHERING,
    )
    sold_at = models.DateTimeField('Час продажу', auto_now=True)

    @property
    def total(self) -> float:
        return sum((product.total_price for product in self.products.all()))
    
    @property
    def margin(self) -> float:
        return sum((product.margin for product in self.products.all()))

    def __str__(self) -> str:
        if self.customer is None:
            return f"Замовлення № {self.pk}"
        else:
            return f"Замовлення № {self.pk} від {self.customer}"
    
    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"