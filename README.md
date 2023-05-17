### 장고 시작하기
파이썬 웹 프레임워크 중 국내에서 자주 사용되는 Django에 대해 학습하려 한다.

### 장고의 장점
#### 1. 쉽고 빠르다
장고는 웹 프로그램을 쉽고 빠르게 만들 수 있도록 도와주는 웹 프레임워크이다. 몇 가지 규칙만 익히면 누구나 빠르게 웹 프로그램을 만들 수 있다. 웹 브라우저에 `Hello World`를 출력하려면 장고가 요구하는 간단한 URL규칙을 정의하고 다음과 같은 함수 하나만 작성하면 된다.

`[장고의 빠른 개발 속도를 보여주는 예시]`
```py
def index(req):
  return HttpResponse("Hello World!")
```

#### 2. 튼튼하다
개발자가 웹 프로그램을 만들 때 가장 어렵게 느끼는 기능 중 하나는 보안 기능이다. 기상천외한 방법으로 웹 사이트를 괴롭히는 세력으로 인해 그런데, 이런 공격에 개발자 홀로 신속하게 대응하기란 무척 어려운 일이다. Django는 이러한 공격을 기본으로 잘 막아주기에 **튼튼하다**고 언급한 것이다. 예를 들어 SQL인젝션, XSS, CSRF,, 클릭재킹과 같은 보안 공격을 기본으로 막아준다.
> - SQL인젝션은 악의적인 SQL을 주입하여 공격하는 방법이다.
> - XSS는 자바스크립트를 삽입해 공격하는 방법이다.
> - CSRF는 위조된 요청을 보내는 공격 방법이다.
> - 클릭재킹은 사용자가 의도하지 않은 클릭을 유도하는 공격 방법이다.

### Django 설치

### Django 프로젝트 생성
아래의 명령어로 Django 프로젝트를 생성한다.
```
django-admin startproject config .
```
config 뒤의 . 기호는 현재 디렉토리를 의미한다. 위 명령의 의미는 현재 디렉토리인 projects를 기준으로 프로젝트를 생성하겠다는 뜻이다. 프로젝트가 생성되면 projects 디렉토리 밑에는 장고가 필요로 하는 여러 디렉터리와 파일들이 생성된다.

### 서버 실행
서버 실행은 아래의 명령어로 실행한다.
```
python manage.py runserver
```
터미널을 살펴보면 `http://127.0.0.1:8000`의 주소로 서버가 실행되는것을 확인할 수 있다.

### 앱 생성
프로젝트를 생성했으나, 프로젝트 단독으로는 그 어떤것도 할 수 없다. 프로젝트에 기능을 추가하기 위해서는 앱을 생성해야 한다. 이제 게시판 기능을 담당할 pybo라는 앱을 생성해보자.
```
django-admin startapp pybo
```

이후 상세한 정보들은 Markdown 폴더를 확인할 것.