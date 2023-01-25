import datetime

from django.db import models
from django.utils import timezone

# Create your models here.


# 모델 -> 부가적인 메타데이터를 가진 데이터베이스의 구조, class로 표현
class Question(models.Model):  # question 은 choice 와 다대일관계(질문 한개에 선택지는 여러개)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):  # shell 뿐만 아니라 admin 페이지를 위해서도 필요한 함수
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Person(models.Model):
    # GenderType = models.TextChoices('GenderType*', 'Male Female Other') # enum 만들어줌
    # 변수이름은 GenderType, enum 이름은 GenderType*, choices는 Male Female Other
    # gender = models.CharField(blank=True, choices=GenderType.choices, max_length=10)

    GENDER = (('M', 'Male'), ('F', 'Female'), ('O', 'Other'))
    gender = models.CharField(max_length=1, choices=GENDER)
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f'INFO : {self.name}, {self.age}, {self.gender}'

    class Meta:
        abstract = True


class Voter(Person):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    vote_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return super().__str__() + f'\n  Q. {self.choice.question} A. {self.choice}\n voted at {self.vote_date}'
        # self.choice로 question 갖고올수 없을까? -> self.choice.question , ~.question.question_text 둘다됌
        # 각 클래스마다 __str__ 함수를 재정의 해놓았기 떄문에 출력시 제대로된 정보가 나오는 것임.


# python manage.py makemigrations appName -> 특정 app의 models.py 에 정의된 Class를 이용하여 모델을 새로 생성하거나 수정한 부분을 migration(sql 문을 생성시킬 수 있는 클래스)형태로 저장함

# python manage.py sqlmigrate appName migrationNumber -> migration 형태로 저장된 모델의 생성 혹은 변경점을 실제 sql 문으로 생성했을 때, 어떤 sql 문이 생성되는지 보여줌(실제 데이터베이스에 반영한 것이 아님)

# python manage.py migrate -> 실제 데이터베이스에 적용되지 않은 마이그레이션을 수집에 실행하며 모델의 생성 혹은 변경점들을 실제 데이터베이스의 스키마에 적용시키며 동기화 시킴

# queryset.query -> queryset에 의해 생성되는 실제 query를 확인할 수 있음.

# 새로운 레코드를 데이터베이스에 추가하고자 할때 -> 생성자 + 인스턴스이름.save() or create() 메서드(create는 save까지 포함됌)
# 만약 외래키를 포함하는 레코드가 있다면, 외래키를 포함하는 원본 레코드를 먼저 생성 후, 그 원본 레코드를 필드값으로 넣어서 새로운 또 다른 레코드를 만든다. (ex. voter 를 만들기 위해 choice를 먼저 만들어야하고, choice를 만들기 위해 question을 먼저 만들어야한다.)

# 1. 생성자 : ClassName(field1 = value1, field2 = value2, ...)
# ex) Question(~필드 생략~) -> 참조관계를 갖는 필드가 없으니까 걍 이렇게 해도 만들 수 있음, Choice는 먼저 만들어놓은 Question을 생성자의 인자로 넘겨야함. Choice(quesetion=미리만들어놓은_question_인스턴스, ~나머지필드생략~)

# 2-1. create() 메서드 : ClassName.objects.create(field1 = value1, field2 = value2, ...)
# ex) Question.objects.create(~필드 생략~), Choice.objects.create(quesetion=미리만든_question_인스턴스, ~나머지~)
# -> 만약 필드중에 참조의 관계를 가지는 필드가 있다면, 먼저 그 필드에 해당하는 레코드를 생성한 후, 그 레코드를 필드의 값으로 넣는다

# 2-2. (만들고자 하는 레코드가 참조의 관계에 있는 경우) 참조관계에_있는_특정레코드.참조모델이름_set.create(나머지 필드)
# ex) q.choice_set.create(~나머지 필드~) -> 이 경우 choice의 question 필드가 이미 q로 들어간거임.
# -> 참조 관계에 있는 특정 레코드를 골라서, 그 레코드 값을 필드 값으로 갖는 새로운 레코드를 만든다.

# ForeignKey로 어떠한 model A를 참조하고 있는 model B는 그 model A에 접근할 때 미리 ForeignKey로 지정해두었던 변수를 통해 접근할 수 있고, 참조당하고 있는 모델 A는 모델 B에 접근할 때 모델명(소문자)b_set의 형태로 접근한다.

# 필요한 열(column, that is, field)만 골라서 조회 -> values(), values_list(), only
# 1. Voter.objects.filter(condition).values('field1','field2',...) -> {필드 이름 : 필드 값}(딕셔너리) 형태로 반환함
# 2. Voter.objects.filter(condition).values_list('field1','field2',...) -> (필드 값)(튜플) 형태로 반환함
# 3. Voter.objects.filter(condition).only('field1','field2',...) -> 조건으로 입력한 필드 종류 + id 까지 반환함

# __(언더바 2개): 접근하고자하는 변수가 참조하고 있는 다른 모델의 변수일 때, 접근을 위해 사용(외래키 모델 속성의 참조) + 필드 조회
#  ex) ~.filter(question(choice 내부에 선언되어있는 참조중인 변수)__question_text(question 내부에 선언되어있는 변수))
# -> choice 가 question 참조를 위해 choice 클래스 내부에 question 이라는 변수를 만들었지만, question != question_text 이므로, 'question__question_text' 의 방식으로 접근한다.
# .(클래스 멤버 접근 연산자) 와 __(django의 api 에서 멤버를 접근하는 방법)가 사용되는 구간을 확실하게 구분할 수 있어야함
# model_Name.objects.filter(*__조회방법 = '필드값')


# union, intersection 과 같은 집합류 연산을 사용하려면, 각 queryset의 모델이 같거나, 다른 경우, 각 queryset에 포함된 필드와 데이터 유형이 일치해야함. -> 다른 모델이더라도 필드 이름과 데이터 유형이 일치하는 필드만 골라서 집합류 연산 사용 가능

# OR -> queryset_1 | queryset_2 , filter(Q(condition_1)|Q(condition_2))
# 1. Voter.objects.filter(condition_1)|Voter.objects.filter(condition_2)
# 2. Voter.objects.filter(Q(condition_1)|Q(condition_2))

# AND -> filter(cond_1, cond_2, ...) queryset_1 & queryset_2 , filter(Q(condition_1)&Q(condition_2))
# 1. Voter.objects.filter(condition_1, condition_2)
# 2. Voter.objects.filter(condition_1)&Voter.objects.filter(condition_2)
# 3. Voter.objects.filter(Q(condition_1)&Q(condition_2))

# NOT -> excluded(condition), filter(~Q(condition))
# 1. Voter.objects.exclude(condition)
# 2. Voter.objects.filter(~Q(condition))
# Q를 이용하려면 'from django.db.models import Q' 해야함
