from django.db import models
from django.contrib.auth.models import User

from main.models import Auto, Part


class SelectionStatuses(models.IntegerChoices):
    SENDED = 1, "Очікує на підбір"
    RESPONDED = 2, "Підбір здійснено"
    ACCEPTED = 3, "Підбір прийнято"
    REFUSED = 4, "Підбір відхилено"


class SelectionRequest(models.Model):
    STATUSES = SelectionStatuses

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
    status = models.PositiveSmallIntegerField(
        verbose_name="Статус підбору",
        choices=STATUSES.choices,
        default=STATUSES.SENDED,
    )

    requested_at = models.DateTimeField(
        verbose_name="Дата подачі заявки",
        auto_now_add=True,
    )
    text = models.TextField(verbose_name="Текст запиту")

    @property
    def is_response_processed(self) -> bool:
        if self.status in (self.STATUSES.ACCEPTED, self.STATUSES.REFUSED):
            return False
        else:
            return True

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