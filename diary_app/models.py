from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
# Create your models here.
DIARY_KIND = (("0", "private"), ("1", "public"))


class User(AbstractUser):
    login = models.CharField(verbose_name="Логин", unique=True, max_length=64)

    first_name = None
    last_name = None
    email = None
    username = None
    is_staff = None
    is_active = None
    date_joined = None
    last_login = None
    is_superuser = None

    USERNAME_FIELD = "login"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.login


class Diary(models.Model):
    title = models.CharField(verbose_name="Название дневника", max_length=256)
    expiration = models.DateTimeField(
        verbose_name="Дата, после которой можно удалить дневник", null=True, blank=True
    )
    kind = models.CharField(
        verbose_name="Тип дневника", choices=DIARY_KIND, default='0', max_length=1
    )
    user = models.OneToOneField(
        User, verbose_name="Пользователь", on_delete=models.CASCADE
    )


class Note(models.Model):
    diary = models.ForeignKey(Diary, verbose_name="Дневник", on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст страницы")


