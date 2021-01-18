from django.shortcuts import render
from django.views import generic
from django.utils import timezone

from .models import Question


# Create your views here.
class IndexView(generic.ListView):
	models = Question
	context_object_name = 'questions'
	template_name = 'quiz/index.html'
	
	def get_queryset(self):
		return Question.objects.filter(
								question_date__lte=timezone.now()
							).order_by('question_date')