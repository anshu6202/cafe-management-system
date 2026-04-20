"""
Custom Permissions for API endpoints
"""

from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission to allow only admins to edit, anyone can view.
    """

    def has_permission(self, request, view):
        # Allow any access method to safe methods
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only allow POST, PUT, PATCH, DELETE by admins
        return request.user and request.user.is_staff


class IsAdminUser(permissions.BasePermission):
    """
    Permission to allow only admin users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission to allow only the owner or admin to edit.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to anyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner or admin
        if hasattr(obj, 'user'):
            return obj.user == request.user or request.user.is_staff
        
        return request.user.is_staff


class IsOwner(permissions.BasePermission):
    """
    Permission to allow only the owner to access.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False


class IsAuthenticatedAndNotAnonymous(permissions.BasePermission):
    """
    Permission to ensure user is authenticated.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class AllowAnyPublic(permissions.BasePermission):
    """
    Allow any access.
    """

    def has_permission(self, request, view):
        return True
