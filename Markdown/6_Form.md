### 질문 등록하기
질문을 등록해보자. 우선 아래의 url pattern을 하나 삽입한다.

`[projects/web/pybo/urls.py]`
```py
(... 생략 ...)
path('question/create/', views.question_create, name='question_create') # 추가
(... 생략 ...)
```

또한 이 별칭을 이용하는 버튼을 하나 생성하자.

`[projects/web/templates/question_list.html]`
```html
(... 생략 ...)
</table>
  <a href="{% url 'pybo:question_create' %}" class="btn btn-primary">질문 등록하기</a>
</div>
{% endblock %}
```

이렇게 질문 등록화면으로 이동하는 버튼을 생성했다. 이제 Form에 대해서 알아보자.

### Form

폼은 쉽게 말해 페이지 요청 시 전달되는 파라미터들을 쉽게 관리하기 위해 사용하는 클래스이다. 폼은 필수 파라미터의 값이 누락되지 않았는지, 파라미터의 형식은 적절한지 등을 검증할 목적으로 사용한다. 이 외에도 HTML을 자동으로 생성하거나 폼에 연결된 모델을 이용하여 데이터를 저장하는 기능도 있다.

질문 등록 시 사용할 QuestionForm을 아래와 같이 생성해보자.

`[projects/web/pybo/forms.py]`
```py
from django import forms
from pybo.models import Question

class QuestionForm(forms.ModelForm):
  class Meta:
    model = Question # 사용할 모델
    fields = ['subject', 'content'] # QuestionForm에서 사용할 Question모델의 속성
```
QuestionForm 클래스는 현재 forms.ModelForm을 상속하고 있다. 장고의 폼은 일반 폼(forms.Form)과 모델 폼(forms.ModelForm)이 있는데 모델 폼은 모델과 연결된 폼으로 폼을 저장하면 연결된 모델의 데이터를 저장할 수 있는 폼이다. 모델 폼은 이너 클래스인 Meta클래스가 반드시 필요하다. Meta클래스에는 사용할 모델과 모델의 속성을 표기해야 한다.

### View함수 작성하기
현재 `question/create/` url pattern에 매핑된 views.question_create함수는 작성되지 않았다. 그 함수를 작성하자.

`[projects/web/pybo/views.py]`
```py
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question
from .forms import QuestionForm

(... 생략 ...)

def question_create(request):
  form = QuestionForm()
  return render(request, 'pybo/question_form.html', {'form':form})
```
QuestionForm객체를 생성하여 {'form':form}형태로 전달한다. 이는 템플릿에서 질문 등록 시 사용할 폼 엘리먼트를 생성할 때 쓰인다.

### Template 파일 작성
이제 질문 등록 화면을 작성해보자.

`[projects/web/templates/pybo/question_create.html]`
```html
{% extends 'base.html' %}
{% block content %}
<div class="container">
    <h5 class="my-3 border-bottom pb-2">질문등록</h5>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-primary">저장하기</button>
    </form>
</div>
{% endblock %}
```
템플릿에서 사용한 `{{form.as_p}}`의 form은 question_create 함수에서 전달한 QuestionForm의 객체이다. {{form.as_p}}는 폼에 정의한 subject, content 속성에 해당하는 HTML코드를 자동으로 생성한다. 질문 등록하기 버튼을 누르고 질문 등록 페이지로 이동하면 필요한 HTML요소들이 자동으로 생성된 모습을 확인할 수 있다.

### 질문 등록 버튼을 통해 저장하기
현재 버튼을 누르면 아무런 동작도 하지 않는다. 등록할 질문을 저장하는 기능을 구현하자.

`[projects/web/pybo/view.py]`
```py
def question_create(request):
  if request.method == 'POST':
    form = QuestionForm(request.POST)
    if form.is_valid(): # 폼이 유효하다면
      question = form.save(commit=False) # 저장 전 임시저장(현재 시각 입력하여 저장해야함)
      question.create_date = timezone.now() # 저장을 위해 현재 시각 입력
      question.save() # 최종 저장
      return redirect('pybo:index') # index페이지로 push

  else:
    form = QuestionForm()

  context = {'form':form}

  return render(request, 'pybo/question_create.html', context)
```
이 함수는 두 군데에서 사용된다. 첫 번째는 질문 목록에서 `질문 등록하기`버튼을 눌렀을 때, 두 번째는 질문 등록 페이지 이동 후 `저장하기` 버튼을 눌렀을 때.

- 질문 등록하기 버튼을 눌렀을 때 요청 방식은 GET method이다. `<a href="{% url 'pybo:question_create' %}" class="btn btn-primary">질문 등록하기</a>`와 같이 링크를 통해 페이지를 요청 시에는 무조건 GET방식이 사용되기 때문이다. 따라서 이 경우에는 `question_create`함수의 else구문을 타고 질문 등록 화면을 렌더링한다.
- 저장하기 버튼을 눌렀을 때 요청 방식은 템플릿 파일에서 설정했다시피 POST method이다. 
GET방식에서 생성하던 폼 형식과는 다르게 `form=QuestionForm(request.POST)`처럼 request.POST를 인수로 생성했다. request.POST를 인수로 QuestionForm을 생성할 경우에는 request.POST에 담긴 subject, content값이 QuestionForm의 subject, content 값에 자동으로 저장되어 객체가 생성된다. 즉, 사용자가 입력한 값이 들어오는 것이다. if구문을 타고 위의 주석대로 요청을 처리한다.