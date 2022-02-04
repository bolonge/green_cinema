from django.shortcuts import render, redirect
from .models import Movie, Rating
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    # 사용자가 있는지 없는지 판단
    user = request.user.is_authenticated
    # 사용자가 있으면 메인화면
    if user:
        return redirect('/main')
    # 사용자가 없으면 로그인화면
    else:
        return redirect(('/sign-in'))

def main_view(request):
    # 사용자가 있는지 없는지 판단
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            # TweetModel.objects.all() : 트윗 모델에 있는 모든 오브젝트를 불러옴
            all_movie = Movie.objects.all()
            return render(request, 'movie/main.html', {'movie': all_movie})
        else:
            return redirect(('/sign-up'))
    else:
        return redirect('/')

def genre_view(request):
    return render(request, 'movie/genre.html')

def contents_view(request):
    return render(request, 'movie/contents.html')