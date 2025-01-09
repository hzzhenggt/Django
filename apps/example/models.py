from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import BaseModel

User = get_user_model()

class Project(BaseModel):
    """项目模型"""
    name = models.CharField('项目名称', max_length=100)
    description = models.TextField('项目描述', blank=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_projects',
        verbose_name='拥有者'
    )
    members = models.ManyToManyField(
        User,
        related_name='joined_projects',
        verbose_name='项目成员'
    )

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Task(BaseModel):
    """任务模型"""
    STATUS_CHOICES = (
        ('pending', '待处理'),
        ('in_progress', '进行中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    )

    title = models.CharField('标题', max_length=200)
    description = models.TextField('描述', blank=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='所属项目'
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        verbose_name='负责人'
    )
    status = models.CharField(
        '状态',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    due_date = models.DateTimeField('截止日期', null=True, blank=True)

    class Meta:
        verbose_name = '任务'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title 