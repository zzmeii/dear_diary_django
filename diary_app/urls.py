from django.urls import path, include
from .views import *
urlpatterns = [
    path('diary/<int:pk>/', DiaryGetView.as_view()),
    path('diary/list/', DiaryListView.as_view()),
    path('diary/create/', DiaryCreateView.as_view()),
    path('diary/delete/<int:pk>/', DiaryDeleteView.as_view()),
    path('note/<int:pk>/', NoteGetView.as_view()),
    path('note/list/<diary_id>/', NoteListView.as_view()),
    path('note/create/', NoteCreateView.as_view()),
    path('note/delete/<int:pk>/', NoteDeleteView.as_view()),
]