from django.urls import path

from . import views


urlpatterns = [
	path('questions/', views.IndexView.as_view(), name='index'),
]