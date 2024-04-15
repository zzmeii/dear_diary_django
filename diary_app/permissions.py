from rest_framework import permissions

from diary_app.models import Note


class NoteIsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return bool(request.user and request.user.is_authenticated)
            if request.method == 'POST':
                return request.user.diary.pk == request.data.get('diary')
            if request.method == 'DELETE':
                return request.user.diary.pk == Note.objects.filter(
                    pk=request.parser_context.get('kwargs').get('pk')).first().diary_id
        return False

    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return obj.diary.user == request.user


class DiaryIsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return bool(request.user and request.user.is_authenticated)
            if request.method == 'POST':
                return request.user.pk == request.data.get('user')
            if request.method == 'DELETE':
                return request.user.diary.pk == int(request.parser_context.get('kwargs').get('pk'))
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return obj.user == request.user
