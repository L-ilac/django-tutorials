"""tutorials URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # path(route,view(2개 필수), kwargs, name(2개 선택))
    # route -> url 패턴을 가진 문자열(도메인 이름 이후의 경로만 바라봄, 매개변수 보지 않음)
    path('polls/', include('polls.urls')),
    # polls/ 로 요청이 들어올 경우 polls.urls 로 연결한다.
    path('admin/', admin.site.urls),
]
