### URL매핑
아래의 경로에 url pattern을 추가하자  

`[projects/web/config/urls.py]`
```py
from django.contrib import admin
from django.urls import path

from pybo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', views.index)
]
```
`http://127.0.0.1:8000/pybo`라는 주소를 요청받으면 views 파일의 index라는 함수가 실행되도록 매핑했다. 이 때 주의할 점으로는 localhost명과 포트번호는 컴퓨터의 환경에 따라 달라질 수 있기에 생략하고 매핑했고, `pybo`가 아니라 `pybo/`로 매핑한 이유는 url을 정규화하는 django의 기능으로 인한 것이다. 특수한 경우가 아닌경우 모두 이렇게 매핑한다.

### 작동 순서 정리하기
> 1. 브라우저에서 로컬 서버로 http://127.0.0.1:8000/pybo 페이지 요청
> 2. urls.py 파일에서 `pybo/` url매핑을 확인하여 views.py 파일의 index 함수를 호출
> 3. 호출한 결과를 브라우저에 반영

### url 분리하기
현재 구조는 pybo와 관련된 url매핑을 추가할 때 마다 `config/urls.py`파일을 수정해야 한다. 이를 분리해보자. 아래의 파일을 다음과 같이 수정한다.  
`[projects/web/config/urls.py]`
```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls'))
]
```
그리고 파일을 새로 하나 생성한다.
`[projects/web/pybo/urls.py]`
```py
from django.urls import path
from . import views

urlpatterns = [
  path('', views.index)
]
```
이렇게 되면 `http://127.0.0.1:8000/pybo`의 요청이 들어왔을 때, `config/urls.py`에서는 `pybo/urls.py`로 요청을 넘길 것이고, `pybo/urls.py`에서는 `path('', views.index)`에 요청이 대응되어 같은 경로에 있는 views파일의 index함수가 실행될 것이다.