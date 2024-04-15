from django.urls import path, include
from rest_framework.routers import Route, SimpleRouter

from .views import *


router = SimpleRouter()
router.register('diary', DiaryModelViewSet, basename='diary')

router.register('note', NoteModelViewSet, basename='note')

urlpatterns = [
    # path('diary/<int:pk>/', DiaryModelViewSet.as_view({'get': 'retrieve'}), name='diary_detail'),
    # path('diary/list/', DiaryModelViewSet.as_view({'get': 'list'}), name='diary_list'),
    # path('diary/create/', DiaryModelViewSet.as_view({'post': 'create'}), name='diary_create'),
    # path('diary/delete/<int:pk>/', DiaryModelViewSet.as_view({'delete': 'destroy'}), name='diary_delete'),
    # path('note/<int:pk>/', NoteModelViewSet.as_view({'get': 'retrieve'}, name='note_detail')),
    # path('note/list/<diary_id>/', NoteModelViewSet.as_view({'get': 'list'}, name='note_list')),
    # path('note/create/', NoteModelViewSet.as_view({'post': 'create'}, name='note_create')),
    # path('note/delete/<int:pk>/', NoteModelViewSet.as_view({'delete': 'destroy'}, name='note_delete')),
] + router.urls

