from django.urls import path

from . import views



app_name = 'pm'

urlpatterns = [
	path('register/', views.register, name='register'),
	path('login/', views.login, name='login'),
	path('validate_registration/', views.validate_registration, name='validate_register'),
	path('validate_login/', views.validate_login, name='validate_login'),
	path('<int:pk>/home/', views.IndexView.as_view(), name='index'),
	path('<int:user_id>/<int:account_id>/remove/', views.remove_account, name='remove'),
	path('<int:user_id>/add/', views.add_account, name='add'),
]