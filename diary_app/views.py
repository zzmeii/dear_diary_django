from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from rest_framework.viewsets import ModelViewSet

from .models import Diary, Note
from .permissions import DiaryIsOwner, NoteIsOwner
from .serializers import DiarySerializer, NoteSerializer


class DiaryModelViewSet(ModelViewSet):
    serializer_class = DiarySerializer
    permission_classes = [DiaryIsOwner]
    queryset = Diary.objects.all()
    filter_fields = ('title', 'expiration', 'kind', 'user')

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class NoteModelViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [NoteIsOwner]
    queryset = Note.objects.all()
    filter_fields = ('diary', 'text')

    @action(detail=True, methods=['get'])
    def notes_in_diary(self, request, diary_pk=None):
        self.queryset = self.queryset.filter(diary_id=diary_pk)
        return super().list(request)

