from django.shortcuts import render
from .models import Question

def index(request):
  # order_by : 조회 결과 정렬함수. create_date앞에 -가 붙었기에 역순으로 정렬하는것을 의미한다.
  question_list = Question.objects.order_by('-create_date')
  context = {'question_list':question_list}
  # render함수는 질문 목록으로 조회한 question_list데이터를 pybo/question_list.html 파일에 적용하여 HTML을 생성한 후 리턴한다.
  # pybo/question_list.html => 템플릿 파일.
  return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
  question = Question.objects.get(id=question_id)
  context = {'question':question}
  
  return render(request, 'pybo/question_detail.html', context)