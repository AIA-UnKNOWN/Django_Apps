from django.test import TestCase
from django.urls import reverse

from .models import User, Account
# Create your tests here.


class LoginViewTests(TestCase):
	
	def test_login_validation(self):
		user = User.objects.create(
			username='imadmin',
			password='admin123'
		)
		
		url = reverse('pm:index', args=(user.id,))
		response = self.client.get(url)
		
		self.assertEqual(response.status_code, 200)
		
	def test_login_unvalidate(self):
		user = User.objects.create(
			username='imadmin',
			password='admin123'
		)
		
		url_invalid = reverse('pm:index', args=(2,))
		response_invalid = self.client.get(url_invalid)
		
		url_valid = reverse('pm:index', args=(user.id,))
		response_valid = self.client.get(url_valid)
		
		self.assertEqual(response_invalid.status_code, 404)
		self.assertEqual(response_valid.status_code, 200)
	

# Shortcut for creating users

def create_user(username, password):
	return User.objects.create(
		username=username,
		password=password
	)
	
	
class IndexViewTests(TestCase):
	
	def test_user_with_no_accounts(self):
		user = create_user('user12345', 'userpass0000')
		url = reverse('pm:index', args=(user.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(
			user.account_set.all(),
			[]
		)
		
	def test_user_with_accounts(self):
		user = create_user('user12345', 'userpass0000')
		user.account_set.create(
			title='Facebook',
			username='myfbuser',
			password='1234567890'
		)
		url = reverse('pm:index', args=(user.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(
			user.account_set.all(),
			['<Account: Facebook>']
		)
		
	def test_users_with_no_accounts(self):
		user1 = create_user('imuser0001', 'userpass0001')
		user2 = create_user('imuser0002', 'userpass0002')
		response_1 = self.client.get(reverse('pm:index', args=(user1.id,)))
		response_2 = self.client.get(reverse('pm:index', args=(user2.id,)))
		self.assertEqual(response_1.status_code, 200)
		self.assertEqual(response_2.status_code, 200)
		self.assertQuerysetEqual(
			user1.account_set.all(),
			[]
		)
		self.assertQuerysetEqual(
			user2.account_set.all(),
			[]
		)
		
	def test_users_with_accounts(self):
		user1 = create_user('imuser0001', 'userpass0001')
		user1.account_set.create(
			title='Instagram',
			username='mydummyinsta',
			password='dummyinstapass'
		)
		user2 = create_user('imuser0002', 'userpass0002')
		user2.account_set.create(
			title='Twitter',
			username='mydummytwitter',
			password='dummytwitterpass'
		)
		user2.account_set.create(
			title='Wattpad',
			username='storyteller143',
			password='wattpadislife'
		)
		response_1 = self.client.get(reverse('pm:index', args=(user1.id,)))
		response_2 = self.client.get(reverse('pm:index', args=(user2.id,)))
		self.assertEqual(response_1.status_code, 200)
		self.assertEqual(response_2.status_code, 200)
		self.assertQuerysetEqual(
			user1.account_set.all(),
			['<Account: Instagram>']
		)
		self.assertQuerysetEqual(
			user2.account_set.all(),
			['<Account: Twitter>', '<Account: Wattpad>'],
			ordered=False
		)