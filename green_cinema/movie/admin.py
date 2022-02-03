from django.contrib import admin
from .models import Movie, Rating

# Register your models here.
admin.site.register(Movie) # 이 코드가 나의 모델을 Admin에 추가 해 줍니다
admin.site.register(Rating)