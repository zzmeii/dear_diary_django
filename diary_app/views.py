from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.generics import ListAPIView, DestroyAPIView, CreateAPIView
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet

from .models import Diary
from .serializers import *


# Create your views here.
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




class tt(ModelViewSet):
    permission_classes = []
    ...



class DiaryGetView(CustomGetAPIView):
    serializer_class = DiarySerializer
    model = Diary


class DiaryListView(ListAPIView):
    serializer_class = DiarySerializer
    queryset = Diary.objects.all()


class DiaryCreateView(CreateAPIView):
    serializer_class = DiarySerializer


class DiaryDeleteView(CustomDeleteAPIView):
    serializer_class = DiarySerializer
    model = Diary


class NoteGetView(CustomGetAPIView):
    serializer_class = NoteSerializer
    model = Note


class NoteListView(ListAPIView):
    paginate_by = 10
    serializer_class = NoteSerializer
    model = Note
    lookup_url_kwarg = 'diary_id'
    lookup_field = 'diary'

    def get_queryset(self):
        return self.model.objects.filter(diary_id=self.kwargs.get('diary_id'))


class NoteCreateView(CreateAPIView):
    serializer_class = NoteSerializer


class NoteDeleteView(CustomDeleteAPIView):
    serializer_class = NoteSerializer
    model = Note
