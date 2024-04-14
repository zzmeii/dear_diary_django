from django.test import TestCase

from django.test import TestCase
from .models import Diary, User, Note
from .serializers import DiarySerializer
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class DiarySerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(login='testuser', password='testpassword')
        super().setUp()

    def test_valid_serializer_data(self):
        diary_data = {'title': 'Test Diary', 'expiration': '2022-12-31T23:59:59Z', 'kind': '1', 'user': self.user.pk}
        serializer = DiarySerializer(data=diary_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer_data(self):
        diary_data = {'title': 'Test Diary', 'expiration': 'Invalid Date', 'kind': 'Z', 'user': 'Invalid User'}
        serializer = DiarySerializer(data=diary_data)
        self.assertFalse(serializer.is_valid())


class AuthenticationTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(login='testuser', password='12345')

    def test_user_authentication(self):
        url = reverse('token_obtain_pair')
        data = {
            'login': 'testuser',
            'password': '12345'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserTest(TestCase):
    def test_user_str(self):
        user = User.objects.create_user(login='testuser', password='testpassword')
        self.assertEqual(str(user), 'testuser')


def create_test_users(count=100):
    # Creating 100 users

    for i in range(1, 101):
        user = User.objects.create_user(login='testuser' + str(i), password='testpassword' + str(i))
        Diary.objects.create(title='Test Diary ' + str(i), expiration='2022-12-31T23:59:59Z', kind='1', user=user)


def create_notes_to_diary(count=20):
    for obj in Diary.objects.all():

        for i in range(1, count + 1):
            Note.objects.create(diary=obj, text='Test Note ' + str(i))
