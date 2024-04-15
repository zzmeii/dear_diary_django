from django.test import TestCase

from django.test import TestCase
from .models import Diary, User, Note
from .serializers import DiarySerializer
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse


def create_test_users(count=100):
    # Creating 100 users

    for i in range(1, 101):
        user = User.objects.create_user(login='testuser' + str(i) + '@example.com', password='testpassword' + str(i))
        Diary.objects.create(title='Test Diary ' + str(i), expiration='2022-12-31T23:59:59Z', kind='1', user=user)


def create_notes_to_diary(count=20):
    for obj in Diary.objects.all():

        for i in range(1, count + 1):
            Note.objects.create(diary=obj, text='Test Note ' + str(i))


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
        self.user = User.objects.create_user(login='testuser@example.com', password='12345')

    def test_user_authentication(self):
        url = reverse('rest_framework:login')
        data = {
            'login': 'testuser@example.com',
            'password': '12345'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestViews(APITestCase):

    def setUp(self):
        create_test_users()
        create_notes_to_diary()

    def test_diary_list(self):
        client = self.client
        client.force_authenticate(User.objects.first())
        url = reverse('diary-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 100)
        self.assertEqual(len(response.data['results']), 50)

    def test_diary_detail(self):
        client = self.client
        client.force_authenticate(User.objects.first())
        url = reverse('diary-detail', args=[Diary.objects.first().pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Diary 1')
        self.assertEqual(response.data, DiarySerializer(Diary.objects.first()).data)

    def test_diary_create(self):
        user = User.objects.create_user(login='testuser-1@example.com', password='testpassword')
        client = self.client
        client.force_authenticate(user)
        url = reverse('diary-list')
        data = {
            'title': 'Test Diary',
            'expiration': '2022-12-31T23:59:59Z',
            'kind': '1',
            'user': user.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_diary_false_delete(self):
        client = self.client
        client.force_authenticate(User.objects.first())
        response = client.delete(reverse('diary-detail', args=[Diary.objects.last().pk]))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_diary_true_delete(self):
        user = User.objects.first()
        client = self.client
        client.force_authenticate(user)
        response = client.delete(reverse('diary-detail', args=[Diary.objects.get(user=user).pk]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Diary.objects.filter(user=user).first(), None)

    # def test_diary_filters(self):
    #     client = self.client
    #     client.force_authenticate(User.objects.first())
    #     response = client.get(reverse('diary-list') + '?user__id__lt=1')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['count'], 1)

    def test_note_list(self):
        client = self.client
        client.force_authenticate(User.objects.first())
        url = reverse('note-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_note_detail(self):
        client = self.client
        client.force_authenticate(User.objects.first())

        url = reverse('note-detail', args=[Note.objects.first().pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], 'Test Note 1')

    def test_note_true_create(self):
        client = self.client
        user = User.objects.create_user(login='testuser-2@example.com', password='testpassword')
        client.force_authenticate(user)
        diary = Diary.objects.create(title='Test Note', expiration=None, kind='0', user=user)
        diary.save()
        url = reverse('note-list')
        data = {
            'text': 'Test Note',
            'diary': diary.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_note_false_create(self):
        client = self.client
        client.force_authenticate(User.objects.first())
        url = reverse('note-list')
        data = {
            'text': 'Test Note',
            'diary': 100
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_note_false_delete(self):
        client = self.client
        client.force_authenticate(User.objects.first())
        response = client.delete(reverse('note-detail', args=[Note.objects.last().pk]))

        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN )


    def test_note_true_delete(self):
        client = self.client
        client.force_authenticate(User.objects.first())
        response = client.delete(reverse('note-detail',
                                         args=[Note.objects.filter(diary__user=User.objects.first()).first().pk]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEquals(Note.objects.filter(diary__user=User.objects.first()).first(), None)
