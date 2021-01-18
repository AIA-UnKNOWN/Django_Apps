from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect as HRR
from django.views import generic

from .models import Todo


# Create your views here.

class IndexView(generic.ListView):
	template_name = 'todo/index.html'
	context_object_name = 'tasks'
	
	def get_queryset(self):
		return Todo.objects.filter(
			task_date__lte=timezone.now()
		).order_by('task_date')
	
	
def add_task(request):
	now = timezone.now()
	if request.POST['new_task']:
		new_task = Todo(
			task=request.POST['new_task'],
			task_date=now
		)
		new_task.save()
	else:
		index_template = 'todo/index.html'
		return render(request, index_template, {
			'tasks': Todo.objects.filter(
							task_date__lte=timezone.now()
						).order_by('task_date'),
			'error_message': 'Please input some task.'
		})
	return HRR(reverse('todo:index'))
	
def delete_task(request, task_id):
	task = get_object_or_404(Todo, pk=task_id)
	task.delete()
	return HRR(reverse('todo:index'))