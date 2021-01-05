from django.db import models


# Create your models here.

class User(models.Model):
	username = models.CharField(max_length=100)
	password = models.CharField(max_length=200)
	
	def __str__(self):
		return self.username
		
	def username_gt_10_char(self):
		return len(self.username) >= 10
		
	def password_gt_10_char(self):
		return len(self.password) >= 10
	

class Account(models.Model):
	title = models.CharField(max_length=100)
	username = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.title
		