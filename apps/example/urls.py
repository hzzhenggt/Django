from django.urls import path
from .views import ProjectView, TaskView

urlpatterns = [
    path('projects/', ProjectView.as_view()),
    path('projects/<int:pk>/', ProjectView.as_view()),
    path('projects/<int:pk>/hard_delete/', ProjectView.as_view({'delete': 'hard_delete'})),
    path('tasks/', TaskView.as_view()),
    path('tasks/<int:pk>/', TaskView.as_view()),
    path('tasks/<int:pk>/hard_delete/', TaskView.as_view({'delete': 'hard_delete'})),
] 