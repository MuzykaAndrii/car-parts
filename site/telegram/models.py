from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    id = models.IntegerField(
        verbose_name='Ідентифікатор телеграм аккаунта',
        primary_key=True,
    )
    first_name = models.CharField(
        verbose_name="Імя",
        max_length=50,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name="Прізвище",
        max_length=50,
        null=True,
        blank=True,
    )
    username = models.CharField(
        verbose_name="Нікнейм",
        max_length=50,
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="tg_account",
        verbose_name="Користувач",
    )

    def __str__(self) -> str:
        return f"Телеграм: {self.pk} {self.username or ''} {self.first_name} {self.last_name or ''}"

    class Meta:
        verbose_name = "Телеграм аккаунт"
        verbose_name_plural = "Телеграм аккаунти"