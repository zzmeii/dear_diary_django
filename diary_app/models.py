from django.db import models
from django.contrib.auth.models import AbstractUser

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

    USERNAME_FIELD = "login"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.login


class Diary(models.Model):
    title = models.CharField(verbose_name="Название дневника", max_length=256)
    expiration = models.DateTimeField(
        verbose_name="Дата, после которой можно удалить дневник", null=True, blank=True
    )
    kind = models.CharField(
        verbose_name="Тип дневника", choices=DIARY_KIND, db_default=0, max_length=1
    )
    user = models.OneToOneField(
        User, verbose_name="Пользователь", on_delete=models.CASCADE
    )


class Note(models.Model):
    diary = models.ForeignKey(Diary, verbose_name="Дневник", on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст страницы")


"""
Модель Diary:
1.1 Поля
1. title: string
2.1 Название дневника
2.2 Обязательное поле
2. expiration
3.1 Дата, после которой можно удалить дневник
3.2 Может быть назначена только у private дневников
3. kind: enum
4.1 Тип дневника, значения: public, private
4.2 Обязательное поле
4. Связан с user one-to-many. У юзера много дневников, у дневника
один юзер Модель
Note:
1. Поля
2. text: text
3. связан с Diary one-to-many. У дневника много страниц, у страницы один
дневник
Модель User
1. Поля
2. login: string
2.1 Логин пользователя в виде email Обязательное поле
3. password
3.1 Обязательное поле

"""
