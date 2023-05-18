from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
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

def answer_create(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  # request.POST.get('content')는 POST로 전송된 form데이터 중 content항목에 일치하는 값을 의미한다.
  question.answer_set.create(content = request.POST.get('content'), create_date=timezone.now())
  return redirect('pybo:detail', question_id=question.id)