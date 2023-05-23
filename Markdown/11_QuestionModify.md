### 질문 수정
우선 언제 수정되었는지 확인하기 위해 모델에 수정 일자 속성을 추가한다.

`[projects/web/pybo/models.py]`
```py
(... 생략 ...)

class Question(models.Model):
    (... 생략 ...)
    modify_date = models.DateTimeField(null=True, blank=True)
    (... 생략 ...)

class Answer(models.Model):
    (... 생략 ...)
    modify_date = models.DateTimeField(null=True, blank=True)
```
모델에 변경사항이 생기면?
```
(jango) ~projects\web>python manage.py makemigrations
Migrations for 'pybo':
  pybo\migrations\0004_answer_modify_date_question_modify_date.py
    - Add field modify_date to answer
    - Add field modify_date to question

(jango) ~projects\web>python manage.py migrate       
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, pybo, sessions
Running migrations:
  Applying pybo.0004_answer_modify_date_question_modify_date... OK
```
항상 makemigrations를 먼저 실행하고 migrate를 실행해야 함을 잊지 말자.

### 질문 수정 버튼
질문 상세 화면에 다음과 같이 질문 수정 버튼을 생성한다.

`[projects/web/templates/pybo/question_detail.html]`
```html
(... 생략 ...)
<!-- 질문 -->
<h2 class="border-bottom py-2">{{ question.subject }}</h2>
<div class="card my-3">
    <div class="card-body">
        <div class="card-text" style="white-space: pre-line;">{{ question.content }}</div>
        <div class="d-flex justify-content-end">
            <div class="badge bg-light text-dark p-2 text-start">
                <div class="mb-2">{{ question.author.username }}</div>
                <div>{{ question.create_date }}</div>
            </div>
        </div>
        <div class="my-3">
            {% if request.user == question.author %}
            <a href="{% url 'pybo:question_modify' question.id  %}" 
               class="btn btn-sm btn-outline-secondary">수정</a>
            {% endif %}
        </div>
    </div>
</div>
(... 생략 ...)
```
질문 수정 버튼은 로그인한 사용자와 글쓴이가 같은 경우에만 노출되도록 `{% if request.user == question.author %}`과 같은 조건문을 걸었다.

### urls.py
`pybo:question_modify`라는 url이 추가됨에 따라 새로운 url pattern을 등록한다.

`[projects/web/pybo/urls.py]`
```py
urlpatterns = [
    (... 생략 ...)
    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
]
```

### views.py
`views.question_modify`는 아직 작성하지 않은 함수이다. 이를 작성하자.

`[projects/web/pybo/views.py]`
```py
from django.contrib import messages

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
```
로그인한 사용자와 수정버튼을 누른 사용자가 다를 경우를 대비하여 `messages`라는 모듈을 활용해 "수정권한이 없습니다"라는 오류를 발생시킨다. `messages`모듈은 Django에서 제공하는 모듈로, 넌필드 오류를 발생시킬 경우에 사용한다.

질문 상세 화면에서 "수정"버튼을 클릭하면 `http://localhost:8000/pybo/question/modify/2/`페이지가 GET방식으로 호출되어 질문 수정 화면이 보여진다. 그 화면은 질문 생성 화면과 동일하다. 그리고 질문 수정 화면에서 저장하기 버튼을 누르면 `http://localhost:8000/pybo/question/modify/2/`페이지가 POST방식으로 호출되어 데이터가 수정된다. 

GET요청인 경우, 이전까지는 `QuestionForm`에 아무런 인자 없이 생성했었지만, 질문 수정 화면에 조회된 질문의 제목과 내용이 반영될 수 있도록 다음과 같이 폼을 생성해야한다.
```py
form = QuestionForm(instance = question)
```
폼 생성시 이처럼 `instance`값을 지정하면 폼의 속성 값이 instance의 값으로 채워진다. 따라서 질문을 수정하는 화면에서는 제목과 내용이 채워진 채로 보일 것이다.

POST요청인 경우, 수정된 내용을 반영해야 하는 케이스이므로 다음처럼 폼을 생성해야 한다.
```py
form = QuestionForm(request.POST, instance = question)
```
위 코드의 의미는 instance를 기준으로 form을 생성하지만 `request.POST`의 값으로 덮어쓰라는 의미이다. 따라서 질문 수정화면에서 제목 또는 내용을 변경하여 POST요청을 진행하면 변경된 내용이 QuestionForm에 저장될 것이다.

그리고 질문의 수정일시는 현재 시각으로 설정되게끔 했다.

### 오류 표시
아까 사용했던 messages모듈의 메세지가 발생할 수 있도록 오류 영역을 상단에 추가하자.

`[projects/web/templates/question_detail.html]`
```html
{% extends 'pybo/base.html' %}
{% block content %}
<div class="container my-3">
    <!-- message 표시 -->
    {% if messages %}
    <div class="alert alert-danger my-3" role="alert">
    {% for message in messages %}
        <strong>{{ message.tags }}</strong>
        <ul><li>{{ message.message }}</li></ul>
    {% endfor %}
    </div>
    {% endif %}
    <h2 class="border-bottom py-2">{{ question.subject }}</h2>
  (... 생략 ...)
```