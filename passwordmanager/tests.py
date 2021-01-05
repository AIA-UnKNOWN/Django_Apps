from django.test import TestCase
from django.urls import reverse

from .models import Account
# Create your tests here.

class AccountIndexViewTests(TestCase):
	
	def test_no_accounts(self):
		url = reverse('pm:index')
		response = self.client.get(url)
		
		self.assertContains(response, "No accounts are available.")
		self.assertQuerysetEqual(
			response.context['accounts'],
			[]
		)
		
	def test_account(self):
		Account.objects.create(
			title="My Facebook",
			username="myfbuser",
			password="12345"
		)
		url = reverse('pm:index')
		response = self.client.get(url)
		
		self.assertQuerysetEqual(
			response.context['accounts'],
			['<Account: My Facebook>']
		)
		
	def test_accounts(self):
		Account.objects.create(
			title="Youtube", 
			username="cathcath101",
			password="xxx0000xxx"
		)
		Account.objects.create(
			title="Facebook",
			username="catherine101",
			password="100100100"
		)
		
		url = reverse('pm:index')
		response = self.client.get(url)
		
		self.assertQuerysetEqual(
			response.context['accounts'],
			['<Account: Youtube>', '<Account: Facebook>'],
		)