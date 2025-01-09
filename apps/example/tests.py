from django.test import TestCase
from django.contrib.auth.models import User
from apps.example.models import Project, Task

class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.project = Project.objects.create(name='Test Project', description='This is a test project', owner=self.user)

    def test_project_creation(self):
        self.assertEqual(self.project.name, 'Test Project')
        self.assertEqual(self.project.description, 'This is a test project')
        self.assertEqual(self.project.owner, self.user)

    def test_project_update(self):
        self.project.name = 'Updated Project'
        self.project.save()
        updated_project = Project.objects.get(id=self.project.id)
        self.assertEqual(updated_project.name, 'Updated Project')

    def test_project_delete(self):
        self.project.delete()
        with self.assertRaises(Project.DoesNotExist):
            Project.objects.get(id=self.project.id)

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.project = Project.objects.create(name='Test Project', description='This is a test project', owner=self.user)
        self.task = Task.objects.create(title='Test Task', description='This is a test task', project=self.project, assignee=self.user)

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'This is a test task')
        self.assertEqual(self.task.project, self.project)
        self.assertEqual(self.task.assignee, self.user)

    def test_task_update(self):
        self.task.title = 'Updated Task'
        self.task.save()
        updated_task = Task.objects.get(id=self.task.id)
        self.assertEqual(updated_task.title, 'Updated Task')

    def test_task_delete(self):
        self.task.delete()
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=self.task.id)
