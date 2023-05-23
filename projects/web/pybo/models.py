from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
  author = models.ForeignKey(User, on_delete = models.CASCADE)
  subject = models.CharField(max_length = 200)
  content = models.TextField()
  create_date = models.DateTimeField()
  modify_date = models.DateTimeField(null=True, blank=True)
  
  def __str__(self):
    return self.subject
  
class Answer(models.Model):
  # Answer는 질문에 대한 답변에 대한 모델이기에 Question 모델을 속성으로 가져가야 한다.
  # 기존 모델을 속성으로 연결하려면 외래키(ForeignKey)를 사용해야 한다. 
  # on_delete=models.CASCADE의 의미는 답변과 연결된 질문이 삭제될 경우 답변도 함께 삭제된다는 의미이다.
  author = models.ForeignKey(User, on_delete = models.CASCADE)
  question = models.ForeignKey(Question, on_delete = models.CASCADE)
  content = models.TextField()
  create_date = models.DateTimeField()
  modify_date = models.DateTimeField(null=True, blank=True)
