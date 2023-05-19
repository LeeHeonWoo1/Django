### Pagination
장고의 페이징처리를 진행한다. 장고에서는 `Paginator`라는 클래스를 활용하여 페이징 처리를 진행한다.

`[projects/web/pybo/views.py]`
```py
(... 생략 ...)
from django.core.pagination import Pagination

def index(request):
  page = request.GET.get('page', '1') # 페이지
  question_list = Question.objects.order_by('-create_date')
  paginator = Paginator(question_list, 10) # 페이지 당 10개의 게시글씩 표현
  page_obj = paginator.get_page(page)
  context = {'question_list':page_obj}

  return render(request, 'pybo/question_list.html', context)

(... 생략 ...)
```
page변수에는 GET방식으로 호출된 url로부터 가져온 page값을 할당했고, 만약 page값 없이 호출될 경우에는 기본값인 `'1'`을 설정해서 1페이지로 이동하게끔 작성했다.  

또한 Paginator 클래스는 다음과 같이 사용되었다.
```py
paginator = Paginator(question_list, 10)
```
Paginator 클래스의 첫 번째 인자는 보여줄 전체 게시글을 의미하고, 두 번째 인자는 한 페이지당 보여질 게시글의 수를 의미한다.

```py
page_obj = paginator.get_page(page)
```

그리고 paginator를 이용하여 요청된 페이지에 해당되는 페이징 객체인 `page_obj`를 설정했다. 이렇게 하면 장고 내부적으로는 데이터 전체를 조회하지 않고 해당 페이지의 데이터만 조회하도록 쿼리가 변경된다.

페이징 객체인 `page_obj`의 여러가지 속성은 아래 표를 참고하자.

|항목|설명|
|---|---|
|paginator.count|전체 게시물 개수|
|paginator.per_page|페이지 당 보여줄 게시물 개수|
|paginator.page_range|페이지 범위|
|number|현재 페이지 번호|
|previous_page_number|이전 페이지 번호|
|next_page_number|다음 페이지 번호|
|has_previous|이전 페이지 존재 유무|
|has_next|다음 페이지 존재 유무|
|start_index|현재 페이지 시작 인덱스(1부터 시작)|
|end_index|현재 페이지의 끝 인덱스(1부터 시작)|

### Template파일에 적용하기
템플릿 파일에 전달하고 있는 형태는 다음과 같다.
```py
context = {'question_list':page_obj}
return render(request, 'pybo/question_list.html', context)
```
템플릿에 전달되는 페이징 객체는 question_list이다. 이제 페이징 객체인 question_list를 이용하여 템플릿에서 어떻게 페이징을 처리할 수 있는지 살펴보자.

우선 question_list.html 파일을 수정한다.

`[projects/web/templates/pybo/question_list.html]`
```html
<!-- 페이징처리 시작 -->
    <ul class="pagination justify-content-center">
        <!-- 이전페이지가 있다면 -->
        {% if question_list.has_previous %}
          <li class="page-item"> <!-- 버튼을 생성하고 -->
              <a class="page-link" href="?page={{ question_list.previous_page_number }}">이전</a>
          </li>
        {% else %} <!-- 아니라면 -->
          <li class="page-item disabled"> <!-- 버튼을 비활성화 한다 -->
              <a class="page-link" tabindex="-1" aria-disabled="true" href="#">이전</a>
          </li>
        {% endif %}
        <!-- 페이지리스트 -->
        {% for page_number in question_list.paginator.page_range %}
          {% if page_number >= question_list.number|add:-5 and page_number <= question_list.number|add:5 %} <!-- 템플릿 필터를 이용해 현재 페이지 넘버보다 5만큼씩 큰 페이지까지만 버튼 노출 -->
          {% if page_number == question_list.number %} <!-- 페이지 번호가 현재 페이지 번호라면 -->
            <li class="page-item active" aria-current="page"> <!-- 활성화 -->
                <a class="page-link" href="?page={{ page_number }}">{{ page_number }}</a>
            </li>
          {% else %} <!-- 아니라면 -->
            <li class="page-item"> <!-- 활성화 하지 않은 일반적인 형태 -->
                <a class="page-link" href="?page={{ page_number }}">{{ page_number }}</a>
            </li>
          {% endif %}
          {% endif %}
        {% endfor %}
        <!-- 다음페이지 -->
        {% if question_list.has_next %} <!-- 만약 다음페이지가 존재한다면 -->
        <li class="page-item"> <!-- 버튼을 만들고 -->
            <a class="page-link" href="?page={{ question_list.next_page_number }}">다음</a>
        </li>
        {% else %} <!-- 아니라면 -->
        <li class="page-item disabled"> <!-- 버튼 비활성화 -->
            <a class="page-link" tabindex="-1" aria-disabled="true" href="#">다음</a>
        </li>
        {% endif %}
    </ul>
    <!-- 페이징처리 끝 -->
```