### Login, Logout 구현하기

우선 로그인과 로그아웃 구현 시 사용할 common app부터 다운로드하자.
```
(jango) ~projects\web> django-admin startapp common
```
앱을 다운받는 이름은 내 마음대로 설정할 수 있는데, 왜 common일까? 하나의 웹 사이트에는 파이보와 같은 게시판 서비스 외에도 블로그나 쇼핑몰과 같은 굵직한 단위의 앱들이 함께 있을 수 있기 떄문에 공통으로 사용되는 기능인 로그인이나 로그아웃을 이 중의 하나의 앱에 족속시키는 것은 좋지 않기 때문이다. 이러한 이유로 여기서는 로그인-로그아웃을 "공통 기능을 가진 앱" 이라는 의미에서 common 으로 다운받았다.  

그리고 pybo앱을 다운받은 이후 등록했던 것과 마찬가지로, common 앱도 등록하자.

`[projects/web/config/settings.py]`
```py
(... 생략 ...)
INSTALLED_APPS = [
    'common.apps.CommonConfig', # common 앱 등록
    'pybo.apps.PyboConfig',
    'django.contrib.admin',

(... 생략 ...)
]
```

이어서 common앱의 urls.py파일을 사용하기 위해 아래 파일을 수정한다.

`[projects/web/config/urls.py]`
```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')),
    path('common/', include('common.urls'))  # common/ 으로 시작하는 url은 common 디렉토리의 urls.py 파일에서 처리
]
```

그리고 `common/urls.py`를 작성하자.

`[projects/web/common/urls.py]`
```py
urlpatterns = [
]
```
이제 필요한 기능들을 common/urls.py에 구현할 것이다.

### 로그인 링크 추가하기
현재 네비게이션 바에는 로그인 탭으로 이동하는 링크만 있지 실질적으로 걸려있는 주소는 따로 없는 상태이다. 링크를 만들자.

`[projects/web/templates/navbar.html]`
```html
(... 생략 ...)
<ul class="navbar-nav me-auto mb-2 mb-lg-0">
  <li class="nav-item">
      <a class="nav-link" href="{% url 'common:login' %}">로그인</a>
  </li>
</ul>
(... 생략 ...)
```

### 로그인 view
navbar.html 파일에서 템플릿 태그로 `url 'common:login'`을 작성했기에 `common/urls.py`에 다음과 같은 url 매핑 규칙을 추가한다.

`[projects/web/common/urls.py]`
```py
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'common'

urlpatterns = [
  path('login/', auth_views.LoginView.as_view(), name='login')
]
```
로그인 뷰는 따로 만들 필요 없이 위 코드처럼 `django.contrib.auth`앱의 LoginView를 사용하도록 설정했다.

### 로그인 Template
이후 `http://127.0.0.1:8000/common/login/`에 접속하면 아래와 같은 오류를 발견할 수 있다.

```
(... 생략 ...)
File "C:\Users\OWNER\Desktop\Django\jango\lib\site-packages\django\template\loader.py", line 47, in select_template
  raise TemplateDoesNotExist(", ".join(template_name_list), chain=chain)
django.template.exceptions.TemplateDoesNotExist: registration/login.html
```
`registration/login.html`이라는 템플릿이 존재하지 않는다는 뜻인데, 위에서 사용한 LoginView의 경우 registration이라는 템플릿 디렉토리에서 login.html을 찾는다. 그래서 registration이라는 디렉토리를 만들어야 하지만, 아래의 설정을 통해 파일의 경로를 지정할 수도 있다.

`[projects/web/common/urls.py]`
```py
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'common'

urlpatterns = [
  path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login')
]
```
이렇게 수정하면 이제 registration디렉토리가 아닌 common디렉토리에서 login.html파일을 참조하게 된다.

### 템플릿 디렉토리, 파일 생성
그럼 이제 common템플릿의 디렉토리와 파일을 생성하자.

`[projects/web/templates/common/login.html]`
```html
{% extends "base.html" %}
{% block content %}
<div class="container my-3">
    <form method="post" action="{% url 'common:login' %}">
        {% csrf_token %}
        {% include "form_errors.html" %}
        <div class="mb-3">
            <label for="username">사용자ID</label>
            <input type="text" class="form-control" name="username" id="username"
                   value="{{ form.username.value|default_if_none:'' }}">
        </div>
        <div class="mb-3">
            <label for="password">비밀번호</label>
            <input type="password" class="form-control" name="password" id="password"
                   value="{{ form.password.value|default_if_none:'' }}">
        </div>
        <button type="submit" class="btn btn-primary">로그인</button>
    </form>
</div>
{% endblock %}
```
로그인에 사용되는 사용자ID를 의미하는 username과 비밀번호인 password항목은 `django.contrib.auth` 앱이 요구하는 필수 항목이다.  
그리고 {% csrf_token %} 밑에 include로 포함된 에러 페이지 템플릿 파일을 아래와 같이 작성하자.

`[projects/web/templates/common/form_errors.html]`
```html
<!-- 필드 오류와 넌필드 오류를 출력한다. -->
{% if form.errors %}
<div class="alert alert-danger">
    {% for field in form %}
    <!-- 필드 오류 -->
    {% if field.errors %}
    <div>
        <strong>{{ field.label }}</strong>
        {{ field.errors }}
    </div>
    {% endif %}
    {% endfor %}
    <!-- 넌필드 오류 -->
    {% for error in form.non_field_errors %}
    <div>
        <strong>{{ error }}</strong>
    </div>
    {% endfor %}
</div>
{% endif %}
```
폼 오류에는 두 가지 오류가 존재한다.  
- 필드오류(field.errors) : 사용자가 입력한 필드 값에 대한 오류로, 값이 누락되었거나 필드의 형식이 일치하지 않는 경우에 발생하는 오류
- 넌필드 오류(form.non_field_errors) : 필드의 값과는 상관없이 다른 이유로 발생.

이후 로그인을 수행할 수 있는데, 현재 로그인할 수 있는 계정은 관리자 계정 하나 뿐이다. 이를 통해 로그인을 하면 다음과 같은 오류가 발생한다.
```
[22/May/2023 14:27:38] "POST /common/login/ HTTP/1.1" 302 0
Not Found: /accounts/profile/
```
`django.contrib.auth` 앱은 기본적으로 로그인을 진행하면 `/accounts/profile/`이라는 url로 이동시키기 때문이다. 따라서 아래와 같은 설정을 진행하자.

`[projects/web/config/settings.py]`
```py
(... 생략 ...)

# 로그인 성공 후 이동하는 URL
LOGIN_REDIRECT_URL = '/'
```

### 로그아웃
로그인을 완료하면 로그아웃 링크가 보이게끔 수정해보자.

`[projects/web/templates/navbar.html]`
```html
(... 생략 ...)
<li class="nav-item">
  {% if user.is_authenticated %}
    <a class="nav-link" href="{% url 'common:logout' %}"> {{user.username}} (로그아웃) </a>
  {% else %}
    <a class="nav-link" href="{% url 'common:login' %}">로그인</a>
  {% endif %}
</li>
(... 생략 ...)
```
로그인 시 username이 보이도록 `{{user.username}}`또한 넣어두었다.

> 템플릿에서 user 사용하기
> 뷰 함수에서 템플릿에 User 객체를 전달하지 않더라도 템플릿에서는 `django.contrib.auth` 기능으로 인해 User객체를 사용할 수 있다. 대표적으로 다음과 같은 것들이 있다.
> - user.is_authenticated : 현재 사용자가 인증되었는지 여부(로그인 된 상태라면 true, 로그아웃 상태라면 false)
> - user.is_anonymous : is_authenticated의 반대(로그인한 상태라면 false, 로그아웃 상태라면 true)
> - user.username : 사용자 명(사용자 ID)
> - user.is_superuser : 사용자가 SuperUser인지 여부

이제 로그아웃에 대응하는 URL매핑을 추가하자.

`[projects/web/common/urls.py]`
```py
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
```

또한, 로그아웃 시 이동할 위치도 지정하자.

`[projects/web/config/settings.py]`
```py
(... 생략 ...)

# 로그인 성공 후 이동하는 URL
LOGIN_REDIRECT_URL = '/'

# 로그아웃 시 이동하는 URL
LOGOUT_REDIRECT_URL = '/'
```

로그인, 로그아웃 기능 구현 끝