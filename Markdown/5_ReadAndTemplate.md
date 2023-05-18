### 조회, 템플릿
현재 `http://127.0.0.1:8000/pybo`로 접속하면 문구만 출력되는 것을 확인할 수 있다. 하지만 이 페이지에는 질문 목록이 출력되도록 index함수를 다음과 같이 수정한다.

`[projects/web/pybo/views.py]`
```py
from django.shortcuts import render
from .models import Question

def index(request):
  # order_by : 조회 결과 정렬함수. create_date앞에 -가 붙었기에 역순으로 정렬하는것을 의미한다.
  question_list = Question.objects.order_by('-create_date')
  context = {'question_list':question_list}
  # render함수는 질문 목록으로 조회한 question_list데이터를 pybo/question_list.html 파일에 적용하여 HTML을 생성한 후 리턴한다.
  # pybo/question_list.html => 템플릿 파일.
  return render(request, 'pybo/question_list.html', context)
```

### 템플릿 디렉토리 설정하기
render함수에서 사용한 `pybo/question_list.html`을 작성해야 하는데 그 전에 템플릿 디렉토리부터 설정하자.

`[projects/web/config/settings.py]`
```py
(... 생략 ...)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # 추가
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
(... 생략 ...)
```
DIRS는 템플릿 디렉터리를 여러개 등록할 수 있도록 리스트로 되어있다. `BASE_DIR / 'templates'` 디렉토리 한 개만 등록을 진행한다. BASE_DIR / 'templates'에서 BASE_DIR은 `c:\projects\web`이므로 추가한 디렉토리의 전체 경로는 다음과 같을 것이다.

```
c:\projects\web\templates
```

하지만 이 디렉토리는 없기에 생성해야한다.

장고는 DIRS에 설정한 디렉토리 외에도 앱 디렉토리(pybo)바로 하위에 있는 templates 디렉토리도 템플릿 디렉토리로 인식한다. 즉, 설정을 하지 않아도 `projects\web\pybo\templates`는 템플릿 디렉토리로 인식한다는 것이다. 하지만 이는 권장하는 방법은 아니다.

> 하나의 웹 사이트에서 여러 앱을 사용할 때 여러 앱의 화면을 구성하는 템플릿은 한 디렉터리에 모아 관리하는 편이 여러모로 좋기 때문이다. 예를 들어 앱이 공통으로 사용하는 공통 템플릿을 어디에 저장해야 할지 생각해 보면 왜 이런 방법을 선호하는지 쉽게 이해할 수 있을 것이다.

따라서 pybo앱은 템플릿 디렉토리로 `projects/web/pybo/templates`가 아닌 `projects/web/templates/pybo`디렉토리를 사용할 것이다. 그리고 공통으로 사용하는 템플릿은 `projects/web/templates`에 위치할 예정이다.

- 모든 앱이 공통으로 사용할 템플릿 디렉토리 : `projects/web/templates`
- pybo앱이 사용할 템플릿 디렉토리 : `projects/web/templates/pybo`
- common 앱이 사용할 템플릿 디렉토리 : `projects/web/templates/common`

### Template파일 생성하기
아래 경로에 다음과 같은 파일 생성(없는 디렉토리는 생성할 것)

`[projects/web/templates/pybo/question_list.html]`
```html
{% if question_list %}
    <ul>
    {% for question in question_list %}
        <li><a href="/pybo/{{ question.id }}/">{{ question.subject }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>질문이 없습니다.</p>
{% endif %}
```

#### 템플릿 태그
장고에서 사용하는 템플릿 태그는 크게 3가지가 있다.

- 분기문  
분기문 태그의 사용법은 다음과 같다.  
```html
{% if 조건문1 %}
  <p>조건문1에 해당하는 경우</p>
{%elif 조건문2 %}
  <p>조건문2에 해당하는 경우</p>
{% else %}
  <p>조건문1, 2에 모두 해당되지 않는 경우</p>
{% endif %}
```

- 반복문  
반복문 태그의 사용법은 다음과 같다  
```html
{% for item in List %}
  <p>순서 : {{forloop.counter}} </p>
  <p> {{item}} </p>
{% endfor %}
```
> 분기문과는 다르게 `forloop`이라는 객체를 사용할 수 있다. 자세한 내용은 아래 표를 참고하자.

|forloop 속성|설명|
|---|---|
|forloop.counter|루프내의 순서로 1부터 표시|
|forloop.counter()|루프 내의 순서로 0부터 표시|
|forloop.first|루프의 첫번째 순서인 경우 True|
|forloop.last|루프의 마지막 순서인 경우 True|

- 객체 출력  
객체를 출력하기 위한 태그의 사용법은 아래와 같다.  
```
{{ ObjName }}
```

- 객체 속성 출력  
해당 객체 내에 속성이 존재한다면 `.`를 사용하면 된다.
```
{{ ObjName.attributeName }}
```