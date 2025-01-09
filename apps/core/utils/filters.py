from typing import List
from django.db.models import Q
import operator
from functools import reduce

class BaseFilter:
    """基础过滤器"""
    def filter_queryset(self, request, queryset):
        return queryset

class SearchFilter(BaseFilter):
    """搜索过滤器"""
    def __init__(self, search_fields: List[str]):
        self.search_fields = search_fields

    def filter_queryset(self, request, queryset):
        search_term = request.GET.get('search', '')
        if not search_term or not self.search_fields:
            return queryset
            
        conditions = []
        for field in self.search_fields:
            conditions.append(Q(**{f"{field}__icontains": search_term}))
        return queryset.filter(reduce(operator.or_, conditions))

class OrderingFilter(BaseFilter):
    """排序过滤器"""
    def __init__(self, ordering_fields: List[str]):
        self.ordering_fields = set(ordering_fields)

    def filter_queryset(self, request, queryset):
        ordering = request.GET.get('ordering', '')
        if not ordering:
            return queryset
            
        ordering_fields = [field.strip() for field in ordering.split(',')]
        valid_fields = []
        
        for field in ordering_fields:
            if field.startswith('-'):
                field_name = field[1:]
            else:
                field_name = field
                
            if field_name in self.ordering_fields:
                valid_fields.append(field)
                
        if valid_fields:
            return queryset.order_by(*valid_fields)
        return queryset

class ProjectFilter(BaseFilter):
    """项目过滤器"""
    def filter_queryset(self, request, queryset):
        if not request.user.is_authenticated:
            return queryset.none()
            
        if request.user.is_superuser:
            return queryset
            
        return queryset.filter(
            Q(owner=request.user) | 
            Q(members=request.user)
        ).distinct() 