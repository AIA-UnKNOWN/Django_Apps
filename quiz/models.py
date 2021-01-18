from django.db import models

# Create your models here.
class Question(models.Model):
	question_text = models.CharField(max_length=200, unique=True)
	question_date = models.DateTimeField('date published')
	
	def __str__(self):
		return self.question_text
		
		
class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	answer = models.BooleanField(default=False)
	
	def __str__(self):
		return self.choice_text
		
	def is_the_answer(self):
		return self.answer