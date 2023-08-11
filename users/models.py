from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class CustomUserManager(BaseUserManager):
    def _create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)  # Set is_active to True
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)  # Set is_active to True
        return self._create_user(username, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(unique=True, verbose_name="Телеграм")
    first_name = models.CharField(verbose_name="Имя", **NULLABLE)
    last_name = models.CharField(verbose_name="Фамилия", **NULLABLE)
    chat_id = models.IntegerField(verbose_name="id чата", unique=True, null=True)

    USERNAME_FIELD = "username"
    objects = CustomUserManager()
    REQUIRED_FIELDS = []
