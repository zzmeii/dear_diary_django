from django.http import JsonResponse
from django.shortcuts import render
from rest_auth.views import LoginView

from rest_framework.generics import ListAPIView, DestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet

from .models import Diary
from .serializers import *



# class CustomLoginView(LoginView):
#


class CustomGetAPIView(APIView):
    model = None
    serializer_class = None

    def get(self, request, pk):
        obj = self.model.objects.filter(id=pk).first()
        if obj:
            return JsonResponse(self.serializer_class(instance=obj).data)
        else:
            return JsonResponse({'error': 'Object not found'}, status=HTTP_404_NOT_FOUND)


class CustomDeleteAPIView(DestroyAPIView):
    model = None

    def get_object(self):
        return self.model.objects.filter(id=self.kwargs.get('pk')).first()


class DiaryModelViewSet(ModelViewSet):
    serializer_class = DiarySerializer
    permission_classes = []
    queryset = Diary.objects.all()


class NoteModelViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = []
    queryset = Note.objects.all()

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(diary_id=self.kwargs.get('diary_id'))
        return super().list(request, *args, **kwargs)
