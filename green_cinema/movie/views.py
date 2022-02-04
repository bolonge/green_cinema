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
            # Movie.objects.all() : 무비 모델에 있는 모든 오브젝트를 불러옴
            all_movie = Movie.objects.all()
            return render(request, 'movie/main.html', {'movie': all_movie})
            # test.html 에서 데이터 response 확인 완료
            # return render(request, 'movie/test.html', {'movie': all_movie})
        else:
            return redirect(('/sign-up'))
    else:
        return redirect('/')


def genre_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            # 장르 list
            genre_list = ['Adventure', 'Comedy', 'Action', 'Drama', 'Crime', 'Children', 'Mystery', 'Animation',
                          'Documentary', 'Thriller', 'Horror', 'Fantasy', 'Western', 'Film-Noir', 'Romance', 'Sci-Fi',
                          'Musical', 'War', 'IMAX']
            movie_genre_dict_list = []
            for gen in genre_list:
                # Movie 모델의 오브젝트를 가져 오는데 genre 컬럼 안에 gen이 포함되어 있는 경우만 필터링 해서 가져옴
                movie_list = Movie.objects.filter(genre__contains=gen) # type : list 안에 object / [object, object]
                movie_genre_dict_list.append({gen: movie_list}) # type : 딕셔너리에 gen를 키로 가지고 movie_list를 밸류로 가지는 객체 추가
            return render(request, 'movie/genre.html', {'genre_list': genre_list, 'movie_genre_dict_list': movie_genre_dict_list})
            # test.html에서 데이터 response 확인 완료
            # return render(request, 'movie/test.html', {'genre_list': genre_list, 'movie_genre_dict_list': movie_genre_dict_list})
        else:
            return redirect(('/sign-up'))
    else:
        return redirect('/')


def contents_view(request):
    return render(request, 'movie/contents.html')
