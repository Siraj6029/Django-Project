from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAdminUser


class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.username == obj.username


class IsSuperUserOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsStaffUserOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff
