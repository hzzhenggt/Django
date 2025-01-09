from apps.core.views import CRUDView
from apps.core.permissions import IsAuthenticated, ProjectPermission
from apps.core.utils.filters import ProjectFilter
from .models import Project, Task

class ProjectView(CRUDView):
    model = Project
    fields = ['name', 'description', 'owner', 'members']
    page_size = 10
    permission_classes = [IsAuthenticated, ProjectPermission]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'sort']
    filter_backends = [ProjectFilter]

class TaskView(CRUDView):
    model = Task
    fields = ['title', 'description', 'project', 'assignee', 'status', 'due_date']
    page_size = 10
    permission_classes = [IsAuthenticated, ProjectPermission]
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'created_at', 'sort', 'due_date']
    filter_backends = [ProjectFilter] 