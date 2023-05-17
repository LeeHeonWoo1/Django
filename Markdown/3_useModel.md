### django 셸 사용하기
아래처럼 django 셸을 사용해서 모델을 사용해보자.
```
(jango) ~\projects\web> python manage.py shell
```
일반적인 python 셸과는 다르게 django를 사용하는 데 있어 필요한 사전 설정들이 미리 되어있는 셸이다.  

이제 데이터를 만들어 삽입해보자.
```
>>> from pybo.models import Question, Answer
>>> from django.utils import timezone
>>> question1 = Question(subject="django를 연습하는 중입니다.", content="django를 잘 쓰고싶어요.", create_date = timezone.now())
>>> question1.save()
```

### 데이터 조회하기
위에서 저장한 질문 하나를 조회해보자.

```
>>> Question.objects.all()
```
`Question.objects`를 통해서 Question모델의 데이터들을 조회할 수 있는데, 모든 데이터를 조회하는 함수인 `.all()`을 붙여 데이터를 조회하면 다음과 같은 결과를 얻는다.

`<QuerySet [<Question: Question object (1)>]>`  

id값이 포함되어져서 나오는 모습을 볼 수 있는데, Question모델에 하나의 메소드를 추가하면 표시되는 값을 바꿀 수 있다.  

`projects/web/pybo/models.py`
```py
from django.db import models

class Question(models.Model):
  subject = models.CharField(max_length=200)
  content = models.TextField()
  create_date = models.DateTimeField()

  def __str__(self):
    return self.subject
```

`__str__`메소드를 추가했다. 모델에 변경사항이 발생하면 셸을 재시작해야 변경사항이 반영된다. 똑같이 실행하면 다른 결과를 얻을 수 있다.

`<QuerySet [<Question: django를 연습하는 중입니다.>]>`

### 특정 값 조회하기
특정 값을 조회하기 위해 연습용 데이터 10건을 넣고 시작해보자.  

`[Django Shell]`
```
>>> for i in range(0, 10):
...   question = Question(subject = f"{i}번째 연습용 데이터입니다.", content = f"{i}번째 연습용 본문입니다.", create_date = timezone.now())
...   question.save()

>>> Question.objects.all()
<QuerySet [<Question: django를 연습하는 중입니다.>, <Question: 0번째 연습용 데이터입니다.>, <Question: 1번째 연습용 데이터입니다.>, <Question: 2번째 연습용 데이터입니다.>, <Question: 3번째 연습용 데이터입니다.>, <Question: 4번째 연습용 데이터입니다.>, <Question: 5번째 연습용 데이터입니다.>, <Question: 6번째 연습용 데이터입니다.>, <Question: 7번째 연습용 데이터입니다.>, <Question: 8번째 연습용 데이터입니다.>, <Question: 9번째 연습용 데이터입니다.>]>
```

데이터가 잘 들어간 것을 확인했으면 특정 값에 대한 데이터를 조회해보자. 아래는 특정 id값에 대한 값을 조회하는 것이다.  

```
>>> Question.objects.filter(id=1)
<QuerySet [<Question: django를 연습하는 중입니다.>]>
```
제일 첫 번째로 저장했던 `django를 연습하는 중입니다.`라는 QuerySet이 리턴되는 모습을 볼 수 있다. `filter`함수는 조건에 해당하는 모든 데이터를 리턴하기 때문에 다건(많은 건수)을 의미하는 QuerySet이 반환된다.
그리고 id는 유일한 값이기에 get함수를 통해서도 조회가 가능하다.  

```
>>> Question.objects.get(id=8)
<Question: 6번째 연습용 데이터입니다.>
```
get으로 조회한 결과는 filter와는 다르게 한 건만 리턴한다. get은 반드시 1건의 데이터를 조회할 때 사용한다. 보통 get은 id와 같이 유일한 값으로 조회할 경우에만 사용한다.

### 특정 문자열 포함하는 데이터 조회
```
>>> Question.objects.filter(subject__contains="django")
<QuerySet [<Question: django를 연습하는 중입니다.>]>
```

### 데이터 수정하기
```
>>> q1 = Question.objects.get(id=1)
>>> q1.save
>>> q1
<Question: django를 연습하는 중입니다.>
```

### 데이터 삭제하기
```
>>> q = Question.objects.get(id=1)
>>> q.delete()
(1, {'pybo.Question': 1})
```

### Answer작성
```
>>> q = Question.objects.get(id=2)
>>> q
<Question: Django Model Question>
>>> from django.utils import timezone
>>> a = Answer(question=q, content='네 자동으로 생성됩니다.', create_date=timezone.now())
>>> a.save()
```
우선 작성할 게시글 하나를 불러와서 그 게시글에 댓글과 작성일자를 넣어 save해주었다. 댓글과 연결된 게시글을 조회할 수 있는데, 아래와 같이 작성한다.

```
>>> a.question
<Question: 0번째 연습용 데이터입니다.>
```
또한, 질문에 달린 댓글들 또한 조회가 가능한데, 아래와 같이 한다.

```
>>> q.answer_set.all()
<QuerySet [<Answer: Answer object (1)>]>
```
외래키로 연결된 두 모델이기에 Question -> Answer로의 역방향 접근 또한 가능한 것이다. 