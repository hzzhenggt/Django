from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Project, Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """项目管理"""
    list_display = ['id', 'name', 'owner', 'member_count', 'task_count', 'created_at', 'is_deleted']
    list_filter = ['is_deleted', 'created_at']
    search_fields = ['name', 'description', 'owner__username']
    ordering = ['-sort', '-created_at']
    filter_horizontal = ['members']
    readonly_fields = ['created_at', 'updated_at']
    
    def member_count(self, obj):
        """成员数量"""
        return obj.members.count()
    member_count.short_description = '成员数量'
    
    def task_count(self, obj):
        """任务数量"""
        return obj.tasks.filter(is_deleted=False).count()
    task_count.short_description = '任务数量'
    
    def get_queryset(self, request):
        """包含已删除的记录"""
        return super().get_queryset(request).prefetch_related('members', 'tasks')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """任务管理"""
    list_display = ['id', 'title', 'project_link', 'assignee', 'status', 'due_date', 'created_at', 'is_deleted']
    list_filter = ['status', 'is_deleted', 'created_at', 'due_date']
    search_fields = ['title', 'description', 'project__name', 'assignee__username']
    ordering = ['-sort', '-created_at']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['project', 'assignee']
    
    def project_link(self, obj):
        """项目链接"""
        if obj.project:
            url = reverse('admin:example_project_change', args=[obj.project.id])
            return format_html('<a href="{}">{}</a>', url, obj.project.name)
        return '-'
    project_link.short_description = '所属项目'
    
    def get_queryset(self, request):
        """包含已删除的记录"""
        return super().get_queryset(request).select_related('project', 'assignee')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """外键字段过滤"""
        if db_field.name == "project":
            kwargs["queryset"] = Project.objects.filter(is_deleted=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs) 