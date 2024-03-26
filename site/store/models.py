from django.db import models
from django.contrib.auth.models import User
from django.db.models.query import QuerySet


class OrderStatus(models.IntegerChoices):
    IN_CART = 1, "В корзині"
    SUBMITTED = 2, "Оформлене покупцем"
    IN_TRANSIT = 3, "У процесі доставки"
    IN_DESTINATION = 4, "Замовлення у поштовому відділенні"
    REFUSED = 5, "Замовлення повернено"
    RECEIVED = 6, "Замовлення отримано"
    IN_PROPOSAL = 7, "Запропоновано"


class WithAcceptedStatusesManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(
            status__in=(
                OrderStatus.SUBMITTED,
                OrderStatus.IN_TRANSIT,
                OrderStatus.IN_DESTINATION,
                OrderStatus.REFUSED,
                OrderStatus.RECEIVED,
            )
            ).order_by("-sold_at", "status")


class Order(models.Model):
    STATUSES = OrderStatus

    customer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='orders',
        verbose_name='Замовник',
        null=True,
        blank=True,
    )
    status = models.PositiveSmallIntegerField(
        verbose_name="Статус замовлення",
        choices=OrderStatus.choices,
        default=OrderStatus.IN_CART,
    )
    sold_at = models.DateTimeField('Час продажу', auto_now_add=True, editable=True)

    @property
    def ship_to(self):
        return str(self.customer.shipping_address)

    @property
    def total(self) -> float:
        return sum((product.total_price for product in self.products.all()))
    
    @property
    def total_quantity(self) -> int:
        return sum((product.quantity for product in self.products.all()))
    
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
    
    # order of managers is important
    objects = models.Manager()
    with_accepted_statuses = WithAcceptedStatusesManager()