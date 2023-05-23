from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.http import HttpResponseNotAllowed
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
  page = request.GET.get('page', '1') # 페이지
  # order_by : 조회 결과 정렬함수. create_date앞에 -가 붙었기에 역순으로 정렬하는것을 의미한다.
  question_list = Question.objects.order_by('-create_date')
  paginator = Paginator(question_list, 10) # 페이지 당 10개씩 보여주기
  page_obj = paginator.get_page(page)
  context = {'question_list':page_obj}
  # render함수는 질문 목록으로 조회한 question_list데이터를 pybo/question_list.html 파일에 적용하여 HTML을 생성한 후 리턴한다.
  # pybo/question_list.html => 템플릿 파일.
  return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
  question = Question.objects.get(id=question_id)
  context = {'question':question}
  
  return render(request, 'pybo/question_detail.html', context)

@login_required(login_url="common:login")
def answer_create(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  if request.method == "POST":
    form = AnswerForm(request.POST)
    if form.is_valid():
      answer = form.save(commit=False)
      answer.author = request.user # author 속성에 로그인 계정 저장
      answer.create_date = timezone.now()
      answer.question = question
      answer.save()
      return redirect('pybo:detail', question_id=question.id)
    
  else:
    return HttpResponseNotAllowed('Only POST is possible')
  context = {'question':question, 'form':form}
  return render(request, 'pybo/question_detail.html', context)

@login_required(login_url="common:login")
def question_create(request):
  form = QuestionForm()
  if request.method == 'POST':
    form = QuestionForm(request.POST)
    if form.is_valid():
      question = form.save(commit=False)
      question.author = request.user # author 속성에 로그인 계정 저장
      question.create_date = timezone.now()
      question.save()
      return redirect('pybo:index')
  
  else:
    form = QuestionForm()
  context = {'form':form}
  
  return render(request, 'pybo/question_create.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  if request.user != question.author:
    messages.error(request, "수정 권한이 없습니다.")
    return redirect('pybo:detail', question_id=question_id)
  
  if request.method == "POST":
    form = QuestionForm(request.POST, instance=question)
    if form.is_valid():
      question = form.save(commit = False)
      question.modify_date = timezone.now()
      question.save()
      return redirect('pybo:detail', question_id = question.id)
    
  else:
    form = QuestionForm(instance=question)
  context = {'form':form}
  return render(request, 'pybo/question_create.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  if request.user != question.author:
    messages.error(request, "삭제 권한이 없습니다.")
    return redirect('pydo:detail', question_id=question_id)
  
  question.delete()
  return redirect('pybo:index')

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
  answer = get_object_or_404(Answer, pk = answer_id)
  if request.user != answer.author:
    messages.error(request, "수정 권한이 없습니다.")
    return redirect('pybo:detail', question_id=answer.question.id)
  if request.method == "POST":
    form = AnswerForm(request.POST, instance=answer)
    if form.is_valid():
      answer = form.save(commit=False)
      answer.modify_date = timezone.now()
      answer.save()
      return redirect('pybo:detail', question_id = answer.question.id)
  else:
    form = AnswerForm(instance=answer)
  context = {'answer':answer, 'form':form}
  return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
  answer = get_object_or_404(Answer, pk=answer_id)
  if request.user != answer.author:
    messages.error(request, '삭제 권한이 없습니다.')
  else:
    answer.delete()
  return redirect('pybo:detail', question_id=answer.question.id)