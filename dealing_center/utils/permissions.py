from rest_framework import permissions


class IsSelfUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsUserAuthenticated(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_authenticated()

