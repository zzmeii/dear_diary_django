

from rest_framework.viewsets import  ModelViewSet

from .models import Diary, Note
from .serializers import DiarySerializer, NoteSerializer

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
