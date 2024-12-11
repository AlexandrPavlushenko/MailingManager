from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Введите свой email"
    )
    username = models.CharField(
        max_length=100,
        verbose_name="Username",
        blank=True,
        null=True,
        help_text='Введите свое имя',
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Phone",
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        null=True,
        blank=True,
        help_text="Загрузите аватар",
    )
    country = models.CharField(
        max_length=100,
        verbose_name="Country",
        blank=True,
        null=True,
        help_text='Введите свою страну',)
    is_blocked = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
