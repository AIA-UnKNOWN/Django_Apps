from datetime import timedelta

from django.test import TestCase
from .models import Todo
from django.utils import timezone
from django.urls import reverse


# Create your tests here.

# Shortcut for creating test Todo task
def create_task(task, date):
	return Todo.objects.create(
		task=task,
		task_date=date
	)

class TodoIndexViewTests(TestCase):
	
	def test_status_code(self):
		# Checks if the server is OK
		response = self.client.get(reverse('todo:index'))
		self.assertNotEqual(response.status_code, 404)
		self.assertEqual(response.status_code, 200)
	
	def test_if_task_exist(self):
		# Checks if a given tasks renders in the page
		now = timezone.now()
		create_task("Read a book", now)
		url = reverse('todo:index')
		response = self.client.get(url)
		self.assertQuerysetEqual(
			response.context['tasks'],
			['<Todo: Read a book>']
		)
		
	def test_task_in_future(self):
		# Checks if does't accept a future task
		future = timezone.now() + timedelta(days=30)
		future_task = create_task("Future task", future)
		url = reverse('todo:index')
		response = self.client.get(url)
		
		self.assertIs(future_task.recent_task(), False)
		self.assertContains(response, "No tasks available")
		self.assertQuerysetEqual(
			response.context['tasks'],
			[]
		)
		
	def test_task_in_past(self):
		# Checks if task renders if its in the past
		past = timezone.now() + timedelta(days=-10)
		past_task = create_task("Past task", past)
		url = reverse('todo:index')
		response = self.client.get(url)
		
		self.assertIs(past_task.recent_task(), True)
		self.assertQuerysetEqual(
			response.context['tasks'],
			['<Todo: Past task>']
		)
		
	def test_multiple_tasks(self):
		# Checks for ordered and multiple tasks
		future = timezone.now() + timedelta(days=5)
		past = timezone.now() - timedelta(days=5)
		future_task = create_task("Future task", future)
		past_task = create_task("Past task", past)
		url = reverse('todo:index')
		response = self.client.get(url)
		
		self.assertIs(future_task.recent_task(), False)
		self.assertIs(past_task.recent_task(), True)
		self.assertQuerysetEqual(
			response.context['tasks'],
			['<Todo: Past task>']
		)
		
	def test_no_tasks(self):
		# Tests for no tasks''
		response = self.client.get(reverse('todo:index'))
		self.assertContains(response, "No tasks available")
		self.assertQuerysetEqual(
			response.context['tasks'],
			[]
		)
		
	def test_delete_task(self):
		# Check if the view properly deletes a task
		now = timezone.now()
		task1 = Todo.objects.create(task="Task 1", task_date=now)
		task2 = Todo.objects.create(task="Task 2", task_date=now)
		task1.delete()
		url = reverse('todo:index')
		response = self.client.get(url)
		self.assertQuerysetEqual(
			response.context['tasks'],
			['<Todo: Task 2>']
		)
		