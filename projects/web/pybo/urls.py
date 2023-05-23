from django.urls import path
from . import views

app_name = 'pybo'

urlpatterns = [
  # url 별칭
  # 실무에서 url리팩토링은 빈번하게 일어난다.(ex. /index/question/2 -> index/2/question)
  # 이렇게 되면 url을 수정할 때 마다 해당되는 url을 직접 찾아서 수정해야 하지만 이는 일부 리스크가 있다.
  # 이러한 현상을 방지하기 위해 name이라는 옵션을 사용한다.
  # 하지만 만약 pybo앱 이외에 다른 앱이 프로젝트에 추가되어 같은 별칭명을 사용하게 되면 이는 중복이 발생하기에, 네임스페이스를 의미하는 app_name변수를 위에 작성한다.

  path('', views.index, name='index'), # index라는 별칭 부여
  path('<int:question_id>/', views.detail, name='detail'), # detail이라는 별칭 부여
  path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'), # answer_create라는 별칭 부여
  path('question/create/', views.question_create, name='question_create'),
  path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
  path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),
  path('answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'),
  path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),
  
]