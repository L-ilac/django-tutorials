from django.contrib import admin

# Register your models here.
from .models import Question, Choice, Person, Voter


admin.site.register(Question)  # 특정 모델(데이터베이스)을 관리하는 인터페이스가 필요함을 관리자에게 알려주는 것
admin.site.register(Choice)
admin.site.register(Voter)
