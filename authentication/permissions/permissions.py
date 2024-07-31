from rest_framework import permissions

class IsEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Employer').exists()

class IsYouth(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Youth').exists()