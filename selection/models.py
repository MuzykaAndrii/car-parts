from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

from main.models import Auto, Part


class SelectionRequest(models.Model):
    sender = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="Від користувача",
        related_name="selection_requests",
        null=False,
        blank=False,
    )
    to_car = models.ForeignKey(
        to=Auto,
        verbose_name="До авто",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    requested_at = models.DateTimeField(
        verbose_name="Дата подачі заявки",
        auto_now_add=True,
    )
    text = models.TextField(verbose_name="Текст запиту")

    def __str__(self) -> str:
        return f"Запит {self.pk} від {self.sender}"

    class Meta:
        verbose_name = "Запит на підбір"
        verbose_name_plural = "Запити на підбір"


class SelectionResponse(models.Model):
    request = models.OneToOneField(
        to=SelectionRequest,
        on_delete=models.CASCADE,
        verbose_name="Запит",
        related_name="response",
        null=False,
        blank=False,
    )

    proposal = models.ManyToManyField(
        to=Part,
        verbose_name="Пропозиції",
    )
    text = models.TextField(
        null=True,
        blank=True,
        verbose_name="Коментар",
    )