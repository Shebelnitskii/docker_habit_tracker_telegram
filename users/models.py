from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

NULLABLE = {'blank': True, 'null': True}


# Create your models here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)



class User(AbstractUser):
    username = models.CharField(unique=True, verbose_name='Телеграм')
    first_name = models.CharField(verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(verbose_name='Фамилия', **NULLABLE)
    chat_id = models.IntegerField(verbose_name='id чата', unique=True, null=True)

    USERNAME_FIELD = 'username'
    objects = CustomUserManager()
    REQUIRED_FIELDS = []
