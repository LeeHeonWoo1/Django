### 회원가입 기능 구현하기
우선 회원가입을 위한 링크를 navbar.html 템플릿에 추가하자.

`[projects/web/templates/navbar.html]`
```html
<li>
  {% if not user.is_authenticated %}
  <a class="nav-link" href="{% url 'common:signup' %}">회원가입</a>
  {% endif %}
</li>
```
이제 이 별칭을 사용하는 url매핑 path를 작성하자.

`[projects/web/common/urls.py]`
```py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'), # 회원가입 추가
]
```

### forms.py
views.signup도 없는 함수이기에 생성해야 하지만, 그 전에 회원가입에 사용할 폼을 먼저 생성한다.

`[projects/web/common/forms.py]`
```py
from djagno import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
  email = forms.EmailField(label="이메일")

  class Meta:
    model = User
    fields = ('username', 'password1', 'password2', 'email')
```
현재 `UserForm`은 `UserCreationForm`을 상속받아 만들었다. 이후 email 속성을 추가했다. UserForm을 따로 만들지 않고 UserCreationForm을 사용해도 무관하지만 위처럼 무언가 속성을 추가하기 위해서는 UserCreationForm을 상속하여 만들어야 한다.

상속한 UserCreationForm은 다음과 같은 속성을 가지고 있다.

|속성명|설명|
|---|---|
|username|사용자 이름|
|password1|비밀번호1|
|password2|비밀번호2(비밀번호 1과 일치하는지 대조하기 위한 값)|

UserCreationForm의 is_valid함수는 폼에 위의 속성 3개가 모두 입력되었는지, 비밀번호 1과 비밀번호 2가 같은지, 비밀번호의 값이 비밀번호 생성 규칙에 맞는지 등을 검사하는 로직을 내부적으로 가지고 있다.

### views.py
이제 위에서 작성했던 views.signup 함수를 작성하자.

`[projects/web/common/views.py]`
```py
def signup(request):
  if request.method == "POST":
    form = UserForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      raw_password = form.cleaned_data.get('password1')
      user = authenticate(username = username, password = raw_password) # 사용자 인증
      login(request, user)
      return redirect('index')
    
  else:
    form = UserForm()
  return render(request, 'common/signup.html', {'form':form})
```
POST 요청일 경우 화면에서 입력한 데이터로 사용자를 생성하고 GET요청인 경우에는 회원가입 화면을 보여준다. `form.cleaned_data.get`함수는 폼의 입력값을 개별적으로 얻고 싶은 경우에 사용하는 함수로 여기서는 인증시 사용할 사용자명과 비밀번호를 얻기 위해 사용했다. 그리고 신규 사용자를 생성한 후에 자동 로그인 될 수 있도록 authenticate와 login함수를 사용했다.

> - django.contrib.auth.authenticate : 사용자 인증 담당 함수(사용자 명과 비밀번호가 정확한지 검증)
> - django.contrib.auth.login : 로그인 담당 함수(사용자 세션 생성)

### 회원가입 템플릿
회원가입 화면을 구성한다.

`[projects/web/templates/common/signup.html]`
```html
{% extends "base.html" %}
{% block content %}
<div class="container my-3">
    <form method="post" action="{% url 'common:signup' %}">
        {% csrf_token %}
        {% include "form_errors.html" %}
        <div class="mb-3">
            <label for="username">사용자 이름</label>
            <input type="text" class="form-control" name="username" id="username"
                   value="{{ form.username.value|default_if_none:'' }}">
        </div>
        <div class="mb-3">
            <label for="password1">비밀번호</label>
            <input type="password" class="form-control" name="password1" id="password1"
                   value="{{ form.password1.value|default_if_none:'' }}">
        </div>
        <div class="mb-3">
            <label for="password2">비밀번호 확인</label>
            <input type="password" class="form-control" name="password2" id="password2"
                   value="{{ form.password2.value|default_if_none:'' }}">
        </div>
        <div class="mb-3">
            <label for="email">이메일</label>
            <input type="text" class="form-control" name="email" id="email"
                   value="{{ form.email.value|default_if_none:'' }}">
        </div>
        <button type="submit" class="btn btn-primary">생성하기</button>
    </form>
</div>
{% endblock %}
```