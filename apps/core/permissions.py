from django.http import HttpRequest
from django.db import models
from .exceptions import PermissionError

class BasePermission:
    """基础权限类"""
    def has_permission(self, request: HttpRequest) -> bool:
        """检查是否有权限访问"""
        return True

    def has_object_permission(self, request: HttpRequest, obj: models.Model) -> bool:
        """检查是否有权限访问特定对象"""
        return True

class IsAuthenticated(BasePermission):
    """登录权限"""
    def has_permission(self, request: HttpRequest) -> bool:
        if not request.user or not request.user.is_authenticated:
            raise PermissionError("请先登录")
        return True

class IsOwner(BasePermission):
    """对象所有者权限"""
    owner_field = 'owner'

    def has_object_permission(self, request: HttpRequest, obj: models.Model) -> bool:
        if not request.user or not request.user.is_authenticated:
            raise PermissionError("请先登录")
            
        owner = getattr(obj, self.owner_field, None)
        if owner != request.user:
            raise PermissionError("您不是该对象的所有者")
        return True

class ProjectPermission(BasePermission):
    """项目权限"""
    def has_object_permission(self, request: HttpRequest, obj: models.Model) -> bool:
        if not request.user or not request.user.is_authenticated:
            raise PermissionError("请先登录")
            
        # 超级用户拥有所有权限
        if request.user.is_superuser:
            return True
            
        # 检查项目权限
        project = getattr(obj, 'project', obj)
        if hasattr(project, 'members'):
            if request.user not in project.members.all() and project.owner != request.user:
                raise PermissionError("您不是该项目的成员")
        return True 