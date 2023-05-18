### SuperUser

장고 관리자 기능을 사용해보자. 우선, 장고 관리자 화면에 접속할 수 있는 슈퍼유저를 먼저 생성해야한다. 아래의 명령어를 실행하자.  

```
(jango) ~projects\web> python manage.py createsuperuser
Username (leave blank to use 'owner'): damin
Email address: admin@mysite.com
Password:
Password (again):
Superuser created successfully.
```

다음으로 서버를 구동한 후 `http://127.0.0.1:8000/admin/`페이지에 접속해보자.

### 관리자 페이지에서 모델 관리하기
우선 아래 파일을 수정하자.  

`[projects/web/pybo/admin.py]`
```py
from django.contrib import admin
from .models import Question

admin.site.register(Question)
```
`admin.site.register`로 Question모델을 등록했다. 이후 관리자 페이지에서 Question모델이 등록된 것을 확인할 수 있고 `Add`버튼을 눌러 데이터를 추가할 수도 있다.

### 모델 검색
제목으로 질문데이터를 검색하려 한다. 아래 파일을 다음과 같이 수정하자.

`[projects/web/pybo/admin.py]`
```py
from django.contrib import admin
from .models import Question


class QuestionAdmin(admin.ModelAdmin):
  search_fields = ['subject']


admin.site.register(Question, QuestionAdmin)
```
Question모델에 세부 기능을 추가할 수 있는 QuestionAdmin클래스를 생성하고 제목 검색을 위해 search_field 속성에 'subject'를 추가했다. 관리자 페이지를 새로고침하면 검색창이 삽입된 것을 볼 수 있을 것이다.