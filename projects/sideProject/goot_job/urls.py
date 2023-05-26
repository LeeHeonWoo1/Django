from django.urls import path
from . import views

app_name='goot_jobs'

urlpatterns = [
  path('', views.index, name='home'),
  path('list/', views.get_jobs, name='job_list'),
]