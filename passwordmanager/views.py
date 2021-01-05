from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.http import HttpResponseRedirect as HRR
from django.urls import reverse

from .models import User, Account


# Create your views here.

def register(request):
	return render(request, 'passwordmanager/register.html', {})


def login(request):
	return render(request, 'passwordmanager/login.html', {})
	

def validate_registration(request):
	username = request.POST['username']
	password = request.POST['password']
	confirm_pass = request.POST['confirm-pass']
	
	if not username or not password or not confirm_pass:
		# Renders an error message
		return render(request, 'passwordmanager/register.html', {
			'error_message': 'Please fill the missing fields'
		})
	elif password != confirm_pass:
		# Renders an error message
		return render(request, 'passwordmanager/register.html', {
			'error_message': "Password doesn't match"
		})
	else:
		try:
			User.objects.get(username=username, password=password)
		except User.DoesNotExist:
			User.objects.create(
				username=username,
				password=password
			)
			return HRR(reverse('pm:login'))
		else:
			return render(request, 'passwordmanager/register.html', {
				'error_message': 'Username or Password already exist'
			})


def validate_login(request):
	username = request.POST['username']
	password = request.POST['password']
	
	if not username or not password:
		return render(request, 'passwordmanager/login.html', {
			'error_message': 'Please fill the required fields'
		})
	else:
		try:
			user = User.objects.get(username=username, password=password)
		except User.DoesNotExist:
			return render(request, 'passwordmanager/login.html', {
				'error_message': 'Incorrect username or password'
			})
		else:
			return HRR(reverse('pm:index', args=(user.id,)))

class IndexView(DetailView):
	model = User
	template_name = 'passwordmanager/index.html'
		
		
def add_account(request, user_id):
	title = request.POST['title']
	username = request.POST['user']
	password = request.POST['pass']
	
	user = User.objects.get(pk=user_id)
	
	if title and username and password:
		user.account_set.create(
			title=title,
			username=username,
			password=password
		)
		return HRR(reverse('pm:index', args=(user.id,)))
		
	return HRR(reverse('pm:index', args=(user.id,)))
	
	
def remove_account(request, user_id, account_id):
	user = get_object_or_404(User, pk=user_id)
	try:
		account = user.account_set.get(pk=account_id)
	except Account.DoesNotExist:
		pass
	else:
		account.delete()
		
	return HRR(reverse('pm:index', args=(user.id,)))