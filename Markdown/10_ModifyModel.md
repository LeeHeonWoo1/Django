### 모델 수정
회원 기능이 추가됨에 따라 추가 기능을 구현하려고 한다.

게시판의 질문, 답변에는 누가 글을 작성했는지 알려주는 "글쓴이" 항목이 필요하다. 모델을 수정해서 글쓴이에 해당되는 속성을 추가해보자.

### Question 모델 수정
먼저 Question모데에 author 속성을 추가한다.

`[projects/web/pybo/models.py]`
```py
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
  author = models.ForeignKey(User, on_delete = models.CASCADE) # 추가
  (... 생략 ...)
```
`django.contrib.auth.models`에서 제공하는 User모델(회원 가입 시 데이터 저장에 사용했던 모델과 동일)을 추가했다. 모델의 변동사항을 저장하자.

`[terminal]`
```
(jango) ~projects\web>python manage.py makemigrations
It is impossible to add a non-nullable field 'author' to question without specifying a default. This is because the database needs something to populate existing rows.
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit and manually define a default value in models.py.
Select an option:
```
변동사항을 저장하기 위해 `python manage.py makemigrations`를 실행했더니 위와 같은 선택지가 나왔다. 이는 Question모델에 author를 추가하면 이미 등록되어 있던 게시물에 author에 해당되는 값이 저장되어야 하는데, Django는 author에 어떤 값을 넣어야 하는지 모르기 때문이다. 이러한 문제를 해결하는 방법은 2가지이다.

- 1. author 속성을 null값으로 설정하기
- 2. 기존 게시물에 추가될 author에 강제로 임의 계정 정보를 추가하기.

2번의 방법을 진행하려 한다. 위의 상태를 유지한 채 1을 입력하고 엔터.
```
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit and manually define a default value in models.py.
Select an option: 1
Please enter the default value as valid Python.
The datetime and django.utils.timezone modules are available, so it is possible to provide e.g. timezone.now as a value.
Type 'exit' to exit this prompt
>>> 1
```
그럼 위와 같은 셸이 나타날 것인데, 여기에는 회원 테이블의 id값을 넣어주면 된다.  
> 현재 회원가입으로 데이터를 추가하면 id값은 1씩 늘어나며 저장될 것이다. 나는 1을 입력하고 엔터키를 눌러 우리가 제일 처음 생성했던 SuperUser의 정보를 삽입했다.

이제 변동사항을 데이터베이스에 적용하자.
```
(jango) ~projects\web>python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, pybo, sessions
Running migrations:
  Applying pybo.0002_question_author... OK
```
위 작업을 Answer에도 똑같이 적용해주자.

### author 속성 저장하기
Question, Answer모델에 author 속성이 추가되었기에 이도 함께 저장해주어야 한다.

`[projects/web/pybo/views.py]`
```py
(... 생략 ...)
if form.is_valid():
      answer = form.save(commit=False)
      answer.author = request.user # author 속성에 로그인 계정 저장
      answer.create_date = timezone.now()
(... 생략 ...)
```
이를 question_create 함수에도 똑같이 적용시키자.

### 로그인이 필요한 함수
위 기능을 추가했지만 로그아웃 상태에서 질문 또는 답변을 등록하려 하면 오류가 발생할 것이다. 
```
ValueError: Cannot assign "<SimpleLazyObject: <django.contrib.auth.models.AnonymousUser object at 0x000001834B65B580>>": "Answer.author" must be a "User" instance.
```
이는 `request.user`에 User 객체가 아닌 AnonymousUser 객체가 담겨서 그렇다. 로그아웃 상태에선 request.user에는 AnonymousUser 객체가 담기기 때문이다. 이를 해결하려면 `request.user`를 사용하는 함수에는 `@login_required`라는 어노테이션이 필요하다.

`[projects/web/pybo/views.py]`
```py
(... 생략 ...)
from django.contrib.auth.decorators import login_required
(... 생략 ...)

@login_required(login_url = "common:login")
def answer_create(request, question_id):
  (... 생략 ...)

@login_required(login_url = "common:login")
def question_create(request):
  (... 생략 ...)
```
이러한 어노테이션이 붙은 함수들은 로그인이 필요한 함수가 된다. 만약 로그아웃 상태에서 `@login_required`어노테이션이 붙은 함수들이 호출되면 자동으로 로그인 url로 이동된다.

### next
이렇게 어노테이션을 붙여 객체 불일치 오류는 해결했다. 로그아웃 상태에서 게시글에 댓글등록 버튼을 눌러보면 다음과 같은 url과 함께 로그인 화면으로 이동한다.
```
http://127.0.0.1:8000/common/login/?next=/pybo/answer/create/114/
```
이는 로그인 성공 후 next파라미터에 있는 url페이지로 이동하겠다는 의미이지만 현재는 그렇게 되고 있지는 않다. 템플릿 파일에 hidden타입의 next항목을 추가해줘야 한다.

`[projects/web/templates/common/login.html]`
```html
(... 생략 ...)
<form method="post" action="{% url 'common:login' %}">
    {% csrf_token %}
    <input type="hidden" name="next" value="{{ next }}">  <!-- 로그인 성공후 이동되는 URL -->
    {% include "form_errors.html" %}
(... 생략 ...)
```
이렇게 되면 `<input type="hidden" name="next" value="{{ next }}">`로 /pybo/answer/create는 GET방식으로 호출될 것인데, 현재 views.answer_create에서는 GET방식으로 호출 시 405 error를 일으키고 있다. 이를 바꿔주자.

`[projects/web/pybo/views.py]`
```py
(... 생략 ...)
# from django.http import HttpResponseNotAllowed # 삭제
(... 생략 ...)

@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm() # 405에러가 아니라 화면을 렌더링하게끔
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

(... 생략 ...)
```
그리고 만약 로그아웃 상태에서 댓글을 작성하고 로그인 후 화면으로 다시 돌아오면 작성했던 댓글은 지워진 상태일 것이다. 이러한 현상을 방지하기 위해 로그아웃 상태에서는 댓글을 작성할 수 없게끔 하고, 로그인 후 이용하라는 문구를 넣어보자.

``
```html
(... 생략 ...)
<div class="mb-3">
    <label for="content" class="form-label">답변내용</label>
    <textarea {% if not user.is_authenticated %}disabled{% endif %}
              name="content" id="content" class="form-control" rows="10">{% if not user.is_authenticated %}로그인 후 이용하세요.{% endif %}</textarea>
</div>
<input type="submit" value="답변등록" class="btn btn-primary">
(... 생략 ...)
```