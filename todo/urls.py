from django.urls import path
from . import views


app_name = 'todo'

urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
	path('taskadded/', views.add_task, name='add'),
	path('<int:task_id>/delete/', views.delete_task, name='delete'),
]