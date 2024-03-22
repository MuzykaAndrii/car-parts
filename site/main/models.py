from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from store.models import Order


class CarProducer(models.Model):
    name = models.CharField("Назва", max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f'CarProducer(name={self.name})'

    class Meta:
        verbose_name = "Марка авто"
        verbose_name_plural = "Марки авто"


class Auto(models.Model):
    
    WHEEL_DRIVE_CHOICES = [
        ('1','Повний'),
        ('2','Передній'), 
        ('3','Задній'),   
    ]

    FUEL_CHOICES = [
        ('0','Бензин'),   
        ('1','Електро'),  
        ('2','Дизель'),   
        ('3','Гібрид'),   
    ]
# django.db.utils.IntegrityError: FOREIGN KEY constraint failed
    BODY_CHOICES = [
        ('0','Седан'),    
        ('1','Кросовер'), 
        ('2','Мінівен'),  
        ('3','Мікровен'), 
        ('4','Хетчбек'),  
        ('5','Універсал'),
        ('6','Купе'),     
        ('7','Кабріолет'),
        ('8','Пікап'),    
        ('9','Ліфтбек'),  
        ('10','Фастбек'), 
        ('11','Лімузин'), 
        ('12','Родстер'), 
    ]
    vin = models.CharField('VIN код', max_length=64, primary_key=True)
    model = models.CharField("Модель", max_length=255)
    producer = models.ForeignKey(
        verbose_name="Марка",
        related_name="cars",
        to=CarProducer,
        on_delete=models.CASCADE,
    )
    year_of_production = models.IntegerField("Рік випуску")
    engine_volume = models.FloatField('Об\'єм двигуна')
    wheel_drive = models.CharField('Привід', max_length=255, choices=WHEEL_DRIVE_CHOICES)
    fuel = models.CharField('Тип палива', max_length=255, choices=FUEL_CHOICES)
    body = models.CharField('Тип кузова', max_length=255, choices=BODY_CHOICES)

    owners = models.ManyToManyField(User, related_name="cars")

    @property
    def name(self):
        return f"{self.producer} {self.model}"

    def __str__(self) -> str:
        return f'{self.vin} | {self.producer} {self.model} {self.year_of_production}р.'

    class Meta:
        verbose_name = "Автомобіль"
        verbose_name_plural = "Автомобілі"


class PartProducer(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Імя",
        unique=True,
        blank=False,
        null=False,
    )
    about = models.TextField(
        verbose_name="Опис",
        blank=True,
        null=True,
    )

    def get_absolute_url(self) -> str:
        return reverse("main:part_producer", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Виробник запчастини"
        verbose_name_plural = "Виробники запчастин"


class Part(models.Model):
    name = models.CharField('Назва', max_length=255)
    articul = models.CharField('Артикул', blank=True, max_length=255)
    barcode = models.CharField('Штрих-код', max_length=255)
    
    buy_price = models.FloatField('Закупочна ціна', blank=True)
    sell_price = models.FloatField('Роздрібна ціна', blank=True)

    photo = models.ImageField(
        'Фото товару',
        upload_to="images/products/%Y/%m/%d/",
        blank=True,
        null=True,
    )

    producer = models.ForeignKey(
        PartProducer,
        verbose_name="Виробник",
        related_name="parts",
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    belongs_to = models.ForeignKey(
        verbose_name="Автомобіль",
        related_name="parts",
        to=Auto,
        on_delete=models.CASCADE,
    )

    def get_absolute_url(self):
        return reverse("main:part_detail", kwargs={"part_id": self.pk, "car_vin": self.belongs_to_id})

    def __str__(self) -> str:
        return f'{self.name} ({self.producer}) для {self.belongs_to.name}'
        
    class Meta:
        verbose_name = "Запчастина"
        verbose_name_plural = "Запчастини"


class PartUnit(models.Model):
    part = models.ForeignKey(
        verbose_name="Назва", 
        to=Part,
        on_delete=models.CASCADE
    )
    order = models.ForeignKey(
        Order,
        verbose_name="Замовлення",
        related_name="products",
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name="Кількість",
        default=1,
    )
    buy_price = models.FloatField('Закупочна ціна', blank=True)
    sell_price = models.FloatField('Роздрібна ціна', blank=True)

    @property
    def total_price(self) -> float:
        return self.sell_price * self.quantity
    
    @property
    def margin(self) -> float:
        return (self.sell_price - self.buy_price) * self.quantity

    def save(self, *args, **kwargs) -> None:
        if not self.sell_price:
            self.sell_price = self.part.sell_price
        
        if not self.buy_price:
            self.buy_price = self.part.buy_price

        return super().save(*args, **kwargs)