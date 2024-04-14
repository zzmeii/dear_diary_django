from rest_framework import serializers


class DiarySerializer(serializers.Serializer):
    id =serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True,allow_blank=False,max_length=256)
    expiration = serializers.DateTimeField()
    kind = models.CharField
    user = models.OneToOneField


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