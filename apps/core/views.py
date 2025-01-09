from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
import json

from .utils.pagination import PageInfo
from .utils.cache import cache_response
from .exceptions import ValidationError, NotFoundError
from .permissions import BasePermission, IsAuthenticated
from .utils.filters import SearchFilter, OrderingFilter, ProjectFilter

@method_decorator(csrf_exempt, name='dispatch')
class BaseView(View):
    """基础视图类"""
    model = None
    fields = None
    page_size = 10
    permission_classes = [IsAuthenticated]  # 默认需要登录
    search_fields = []  # 搜索字段
    ordering_fields = []  # 排序字段
    filter_backends = []  # 过滤器
    
    def get_permissions(self):
        """获取权限实例列表"""
        return [permission() for permission in self.permission_classes]
        
    def check_permissions(self, request):
        """检查权限"""
        for permission in self.get_permissions():
            permission.has_permission(request)
            
    def check_object_permissions(self, request, obj):
        """检查对象权限"""
        for permission in self.get_permissions():
            permission.has_object_permission(request, obj)
    
    def get_queryset(self):
        """获取查询集"""
        if not self.model:
            raise NotImplementedError("需要设置model属性")
        queryset = self.model.objects.filter(is_deleted=False)
        
        # 应用过滤器
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(self.request, queryset)
            
        # 应用搜索
        if self.search_fields:
            queryset = SearchFilter(self.search_fields).filter_queryset(self.request, queryset)
            
        # 应用排序
        if self.ordering_fields:
            queryset = OrderingFilter(self.ordering_fields).filter_queryset(self.request, queryset)
            
        return queryset
    
    def get_object(self, pk):
        """获取单个对象"""
        try:
            obj = self.get_queryset().get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except self.model.DoesNotExist:
            raise NotFoundError(f'ID为{pk}的对象不存在')
    
    def json_response(self, data=None, message='success', status=200):
        """统一的JSON响应格式"""
        return JsonResponse({
            'code': status,
            'message': message,
            'data': data
        }, status=status)
    
    def validate_data(self, data):
        """验证数据"""
        if not self.fields:
            return data
            
        validated_data = {}
        for field in self.fields:
            if field not in data:
                raise ValidationError(f'缺少必要字段: {field}')
            validated_data[field] = data[field]
        return validated_data

class CRUDView(BaseView):
    """CRUD视图类"""
    def dispatch(self, request, *args, **kwargs):
        """处理请求前检查权限"""
        self.request = request
        try:
            self.check_permissions(request)
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            return self.json_response(message=str(e), status=getattr(e, 'code', 400))
    
    @cache_response(timeout=300)
    def get(self, request, pk=None):
        """查询"""
        if pk:
            obj = self.get_object(pk)
            return self.json_response(data=obj)
        
        queryset = self.get_queryset()
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', self.page_size))
        page_info = PageInfo(queryset, page, page_size)
        return self.json_response(data=page_info.get_data())
    
    def post(self, request):
        """创建"""
        try:
            data = json.loads(request.body)
            validated_data = self.validate_data(data)
            obj = self.model.objects.create(**validated_data)
            return self.json_response(data=obj, message='创建成功')
        except json.JSONDecodeError:
            raise ValidationError('无效的JSON数据')
        except Exception as e:
            raise ValidationError(str(e))
    
    def put(self, request, pk):
        """更新"""
        obj = self.get_object(pk)
        try:
            data = json.loads(request.body)
            for key, value in data.items():
                setattr(obj, key, value)
            obj.save()
            return self.json_response(data=obj, message='更新成功')
        except Exception as e:
            return self.json_response(message=str(e), status=400)
    
    def delete(self, request, pk):
        """软删除"""
        obj = self.get_object(pk)
        obj.is_deleted = True
        obj.save(update_fields=['is_deleted'])
        return self.json_response(message='删除成功')

    @method_decorator(csrf_exempt, name='dispatch')
    def hard_delete(self, request, pk):
        """硬删除"""
        obj = self.get_object(pk)
        obj.hard_delete()  # 调用模型的硬删除方法
        return self.json_response(message='永久删除成功') 