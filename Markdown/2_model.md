### 모델 작성하기
두 가지 모델을 작성해보자.  

`projects/web/pybo/models.py`
```py
from django.db import models

class Question(models.Model):
  subject = models.CharField(max_length=200)
  content = models.TextField()
  create_date = models.DateTimeField()

class Answer(models.Model):
  question = models.ForeignKey(Question, on_delete = models.CASCADE)
  content = models.TextField()
  create_date = models.DateTimeField()
```
|속성명|설명|
|---|---|
|max_length = 200|필드의 최대 길이를 200으로 제한|
|on_delete = models.CASCADE|참조하는 테이블의 값이 삭제됨에 따라 해당 값도 함께 삭제|

### 작성한 모델을 바탕으로 테이블 생성하기
우선 config/settings.py에 다음 항목을 추가해야 한다.  

`[projects/web/config/settings.py]`
```py
(... 생략 ...)
INSTALLED_APPS = [
    'pybo.apps.PyboConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    (... 생략 ...)
]
(... 생략 ...)
```
생성한 앱 이름(ex. 현재는 django-admin startapp pybo 로 실행했기에 앱 이름=pybo)의 디렉토리의 `apps.py`파일을 확인하면 하나의 클래스가 구현되어 있는 모습을 볼 수 있을 것이다.  

`[projects/web/pybo/apps.py]`
```py
from django.apps import AppConfig

# settings에 추가해야하는 클래스 이름!
class PyboConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pybo'
```
이제 아래의 명령어로 테이블을 생성한다.  

```
(jango) ~\projects\web> python manage.py makemigrations
(jango) ~\projects\web> python manage.py migrate
```
모델이 변경되거나 신규로 생성된다면 `python manage.py makemigrations`로 먼저 수행한 후에 `python manage.py migrate`를 수행해야 한다.