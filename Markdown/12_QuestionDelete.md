### 질문 삭제
질문 삭제 버튼을 생성하자.

`[projects/web/templates/question_detail.html]`
```html
{% if request.user == question.author %}
  <a href="{% url 'pybo:question_modify' question.id  %}" 
  class="btn btn-sm btn-outline-secondary">수정</a>
  <a href="javascript:void(0)" class="delete btn btn-sm btn-outline-secondary"
  data-uri="{% url 'pybo:question_delete' question.id %}">삭제</a>
{% endif %}
```
삭제 버튼은 수정 버튼과는 달리 href속성값을 `javascript:void(0)`로 지정했다.
> href속성값을 javascript:void(0)로 설정하면 해당 링크를 클릭해도 아무런 동작을 하지 않는다.

그리고 삭제를 실행할 URL을 얻기 위해 data-uri 속성을 추가하고, 삭제버튼이 눌리는 이벤트를 확인할 수 있도록 class속성에 delete 항목을 추가했다.
> data-uri 속성은 자바스크립트에서 클릭 이벤트 발생 시 `this.dataset.uri`와 같이 사용하여 그 값을 얻을 수 있다.

### JavaScript
삭제 버튼을 눌렀을 때 확인창을 호출하기 위해서는 아래와 같은 코드가 필요하다.
```html
<script type='text/javascript'>
const delete_elements = document.getElementsByClassName("delete");
Array.from(delete_elements).forEach(function(element) {
    element.addEventListener('click', function() {
        if(confirm("정말로 삭제하시겠습니까?")) {
            location.href = this.dataset.uri;
        };
    });
});
</script>
```
위 코드를 해석하자면, delete라는 클래스를 포함하는 컴포넌트를 클릭하면 확인창이 뜨고, 확인 버튼을 눌렀을 때 해당 컴포넌트의 data-uri값으로 URL호출을 진행하는 것으로 해석할 수 있다. 우리의 경우 삭제 버튼을 클릭하고 확인을 선택하면 data-uri 속성에 해당하는 `{% url 'pybo:question_delete' question.id %}`가 호출될 것이다.

이제 이를 적용하기 위해 base.html부터 수정한다.

`[projects/web/templates/base.html]`
```html
(... 생략 ...)
<script src="{% static 'bootstrap.min.js' %}"></script>
{% block script %}
{% endblock %}
</body>
</html>
```
이제 js코드를 삽입하자.

`[projects/web/templates/pybo/question_detail.html]`
```html
(... 생략 ...)
{% endblock %}
{% block script %}
<script type='text/javascript'>
const delete_elements = document.getElementsByClassName("delete");
Array.from(delete_elements).forEach(function(element) {
    element.addEventListener('click', function() {
        if(confirm("정말로 삭제하시겠습니까?")) {
            location.href = this.dataset.uri;
        };
    });
});
</script>
{% endblock %}
```