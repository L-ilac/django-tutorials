from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse
from django.views import View, generic

from .models import Choice, Question


# Create your views here.

class IndexView(generic.ListView):
    # defalut = "appname/modelname_list.html" -> listview
    template_name = 'polls/index.html'

    # default = question_list (model 이름 기반)
    # context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question  # model 이름 기반 컨텍스트 변수 -> question

    # defalut = "appname/modelname_detail.html" -> detailview
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    test_str = "lilac"
    test_num = 970413
    test_list = [1, 2, 3, 4, 5]

    # 템플릿 파일에 전달할 변수, 딕셔너리의 키값으로 템플릿에서 접근, 템플릿에서 쓸만한 변수들 모두 여기에 포함시켜서 전달
    # context variable -> 컨텍스트 변수
    context = {'question_list': latest_question_list,
               'str': test_str,
               'num': test_num,
               'list': test_list}

    # template = loader.get_template('polls/index.html')  # template 파일 불러오기
    # return HttpResponse(template.render(context, request)) -> 템플릿에서 사용할 데이터(context) 전달

    # 매우 흔한 render의 사용을 위해 만들어진 shortcut
    return render(request, 'polls/index.html', context)
    # render(request, template name, dictionary data(optional))
    # loader, httpresponse 쓸 필요 없음


def detail(request, question_id):  # question_id 는 urls에서 <int:question_id>로 매핑시켜 실제 url의 값을 받아옴
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("question does not exist") -> 404 explanation

    # http404를 위한 shortcut -> 위의 try-except문을 통해 예외처리를 구현하지 않아도됌
    question = get_object_or_404(Question, pk=question_id)
    # get_object_or_404(django의 모델(정의된 클래스), 키워드 인수(어떤 객체를 갖고 올지 정하는 조건))
    # 받은 인수를 get()함수에 전달해서 결과값을 얻어오고, 해당 객체가 존재하지 않으면 http404를 발생시킴
    # 404 explanation -> "no question matches the given query"

    # get_list_or_404() -> 받은 인자들을 get함수 대신 filter 함수에 전달 queryset을 list 접근하듯 접근하면 단일 question 객체임

    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    # question 선택
    question = get_object_or_404(Question, pk=question_id)

    try:
        # post 요청의 body에 실려온 데이터를 딕셔너리 형태로 접근 (항상 문자열 딕셔너리 형태인듯)
        choice_id = request.POST['choice']  # key가 존재하지 않을때 keyerror
        # print(type(choice_id))  # str -> int 형변환 안했음;
        choice = question.choice_set.get(
            pk=choice_id)  # 근데 이게 되네(pk는 int임 왜 작동하는겈ㅋ)

        # choice = get_object_or_404(Choice, pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',
                      {'question': question,
                       'error_message': "you didn't select a choice"})
    else:
        choice.votes += 1
        choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        # redirect() -> httpresponseredirect의 shortcuts

        # reverse 는 view에서 하드코딩된 url을 갖게 되는 것을 방지함
        # reverse('polls:results', args=(question.id,)) -> '/polls/question.id/results' 를 반환

# httpresponse 함수는, 단순히 괄호안에 들어간 값을 브라우저에 출력해줌, 하지만 httpresponse의 값은 하드코드된 페이지 디자인이기 때문에, 사용자의 취향대로 페이지를 디자인하려면 template 을 사용해야함.

# 각각의 뷰는 요청된 페이지의 컨텐츠를 포함하고있는 httpresponse 객체를 반환하거나, http404 같은 예외를 발생시켜야함. 나머지 동작은 맘대로
