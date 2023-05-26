from django.shortcuts import render
from functions.croller_bs4 import get_job_title

# Create your views here.
def index(request):
  return render(request, 'index.html')

def get_jobs(request):
  keyword = request.GET.get('keyword')
  job_list = get_job_title(keyword)
  context = {'job_list': job_list}
  return render(request, 'main/home.html', context)
  