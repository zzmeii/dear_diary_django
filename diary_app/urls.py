from django.urls import path, include
from .views import *
urlpatterns = [
    path('diary/<int:pk>/', DiaryModelViewSet.as_view({'get': 'retrieve'})),
    path('diary/list/', DiaryModelViewSet.as_view({'get': 'list'})),
    path('diary/create/', DiaryModelViewSet.as_view({'create': 'create'})),
    path('diary/delete/<int:pk>/', DiaryModelViewSet.as_view({'delete': 'destroy'})),
    path('note/<int:pk>/', NoteModelViewSet.as_view({'get': 'retrieve'})),
    path('note/list/<diary_id>/', NoteModelViewSet.as_view({'get': 'list'})),
    path('note/create/', NoteModelViewSet.as_view({'create': 'create'})),
    path('note/delete/<int:pk>/', NoteModelViewSet.as_view({'delete': 'destroy'})),
]
