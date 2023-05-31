from django.shortcuts import render
from functions.croller_bs4 import get_job_title

def index(request):
  return render(request, 'index.html')

def get_jobs(request):
  if request.method == 'POST':
    keyword = request.POST.get('keyword')
    result_list = get_job_title(keyword)
    context = {'result_list': result_list}
    return render(request, 'main/home.html', context)
  else:
    return render(request, 'main/home.html')