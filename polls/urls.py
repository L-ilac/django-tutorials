from django.urls import path


from . import views  # . 은 현재 디렉터리

app_name = 'polls'  # 앱이 여러개 있을때, 이름공간을 정해주어 중복된 view name이 있어도 template html 내에서 구분할 수 있게함
# app_name:polls

urlpatterns = [

    # generic view 들은 as_view() 함수를 호출하여 호출됌
    path('', views.IndexView.as_view(), name='index'),

    # detailview 는 pk를 인자로 받음
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),

    # detailview 는 pk를 인자로 받음
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),


    ####################################################################################################

    # domain/polls/
    # path('', views.index, name='index'),

    # # domain/polls/4(<int:question_id>에 매핑될 숫자)
    # path('<int:question_id>/', views.detail, name='detail'),

    # # domain/polls/3(<int:question_id>에 매핑될 숫자)/results
    # path('<int:question_id>/results/', views.results, name='results'),

    # domain/polls/3(<int:question_id>에 매핑될 숫자)/vote
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
