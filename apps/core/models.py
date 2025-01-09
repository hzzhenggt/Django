from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    """基础模型"""
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    desc = models.CharField(max_length=255, verbose_name="描述", null=True, blank=True, help_text="描述")
    sort = models.IntegerField(default=1, null=True, blank=True, verbose_name="显示排序", help_text="显示排序，默认无需填写")
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('是否删除', default=False)

    class Meta:
        abstract = True
        ordering = ['-sort', '-created_at', '-id']

    def delete(self, using=None, keep_parents=False):
        """软删除"""
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])

    def hard_delete(self, using=None, keep_parents=False):
        """硬删除"""
        super().delete(using, keep_parents) 