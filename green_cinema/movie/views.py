from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Rating
from django.contrib.auth.decorators import login_required
from .forms import RatingForm
from random import randrange, shuffle
import csv

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
            all_movie = list(Movie.objects.all())
            shuffle(all_movie)
            movie_shuffle = all_movie
            return render(request, 'movie/main.html', {'movie': movie_shuffle[:50]})
            # test.html 에서 데이터 response 확인 완료
            # return render(request, 'movie/test.html', {'movie': movie_shuffle[:50]})
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
                # type : list 안에 object / [object, object]
                movie_list = Movie.objects.filter(genre__contains=gen)
                # type : 딕셔너리에 gen를 키로 가지고 movie_list를 밸류로 가지는 객체 추가
                movie_genre_dict_list.append({gen: movie_list})
            return render(request, 'movie/genre.html', {'genre_list': genre_list, 'movie_genre_dict_list': movie_genre_dict_list})
            # test.html에서 데이터 response 확인 완료
            # return render(request, 'movie/test.html', {'genre_list': genre_list, 'movie_genre_dict_list': movie_genre_dict_list})
        else:
            return redirect(('/sign-up'))
    else:
        return redirect('/')

# rating 존재 확인 함수 / rating테이블에서 user_id, movie_id가 일치하는 데이터를 리턴, 데이터가 없다면 오류 발생 '0'을 리턴


def existence_rating(request, id):
    try:
        my_rating = get_object_or_404(
            Rating, user_id=request.user.id, movie_id=id)
        return my_rating
    except:
        return '0'


# contents.html(콘텐츠 상세파일) 호출 함수
def contents_view(request, id):
    # 영화 아이디로 Movie 테이블 조회
    contents_movie = Movie.objects.get(id=id)
    check_exist = existence_rating(request, id)
    if check_exist == '0':
        form = RatingForm()
        return render(request, 'movie/contents.html', {'contents_movie': contents_movie, 'form': form, "check_exist": check_exist})
        # return render(request, 'movie/contents_test.html', {'contents_movie': contents_movie, 'form': form, 'ms': '0'})
    else:
        form = RatingForm(instance=check_exist)
        return render(request, 'movie/contents.html', {'contents_movie': contents_movie, 'form': form, 'check_exist': check_exist})
        # return render(request, 'movie/contents_test.html', {'contents_movie': contents_movie, 'form': form, 'ms': '1'})


# rating 생성 함수
@login_required
def rating_create(request, id):
    if request.method == 'POST':  # POST 방식으로 요청이 들어왔을 때
        form = RatingForm(request.POST)  # 입력된 내용들을 form이라는 변수에 저장
        if form.is_valid():  # form이 유효하다면(models.py에서 정의한 필드에 적합하다면)
            # form 데이터를 가져온다. (commit=False : 바로 저장되는 기능을 홀딩)
            rating = form.save(commit=False)
            rating.user_id = request.user
            rating.movie_id = Movie.objects.get(id=id)
            rating.save()  # form 데이터를 DB에 저장한다.
            return redirect('/contents/' + str(id))
        else:
            return redirect('/contents/' + str(id))
    else:  # GET 방식으로 요청이 들어왔을 때
        return redirect('/contents/' + str(id))

# rating 업데이트 함수


@login_required
def rating_update(request, id):
    if request.method == 'POST':
        # rating 테이블에서 user_id, movie_id 일치하는 데이터 가져옴 / update함수는 데이터가 있는 경우에만 호출 되기 때문에 오류뜨면 안됨 / but 나중에 오류처리는 해야될듯?
        my_rating = get_object_or_404(
            Rating, user_id=request.user.id, movie_id=id)
        # form 변수에 request.POST내용을 가져와서 이미 있는 Rating클래스의 인스턴스에(my_rating) 업데이트
        form = RatingForm(request.POST, instance=my_rating)
        if form.is_valid():
            # form 데이터를 가져온다. (commit=False : 바로 저장되는 기능을 홀딩) // 사실 여기서는 바로 저장해도 문제없을듯
            rating = form.save(commit=False)
            rating.save()  # form 데이터를 DB에 저장한다.
            return redirect('/contents/' + str(id))
        else:
            return redirect('/contents/' + str(id))
    else:  # GET 방식으로 요청이 들어왔을 때
        return redirect('/contents/' + str(id))
