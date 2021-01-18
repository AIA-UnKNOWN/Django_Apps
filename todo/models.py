from django.db import models
from django.utils import timezone


# Create your models here.
class Todo(models.Model):
	task = models.CharField(max_length=100)
	task_date = models.DateTimeField('task created')
	
	def __str__(self):
		return self.task
		
	def recent_task(self):
		now = timezone.now()
		return self.task_date <= now