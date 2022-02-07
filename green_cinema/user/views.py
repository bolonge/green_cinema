from hashlib import new
from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model #사용자가 데이터베이스 안에 있는지 검사하는 함수
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from movie.models import Rating
# from .forms import CustomUserChangeForm
from .forms import ProfileForm

        


def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated #로그인 된 사용자가 요청하는 건지
        if user: #로그인 되어있다면
            return redirect('/') #main page로 -> 우리는 index려나?
        else:
            return render(request, 'user/sign-up.html')
    elif request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        username = request.POST.get('username', None)
       
        if email == '' or password == '' or username == '':
            return render(request, 'user/sign-up.html', {'error': '빈칸을 채워주세요 :)'}, )

        elif password != password2:
            return render(request, 'user/sign-up.html', {'error': '인증비밀번호가 맞지 않습니다 ;)'})

        else:
            exist_user = get_user_model().objects.filter(email=email)
            if exist_user:
                return render(request, 'user/sign-up.html', {'error': '이메일이 이미 존재합니다 ;( '})
            else:
                user = UserModel.objects.create_user(email=email, password=password)
                user.username = username
                user.save()
                return redirect('/sign-in') #회원가입이 완료되었으므로 로그인 페이지로 이동
        

def sign_in_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated #사용자가 로그인 되어있는지 검사
        if user:
            return redirect('/')
        else:
            return render(request, 'user/sign-in.html')
    elif request.method == 'POST':
            email = request.POST.get('email',None)
            password = request.POST.get('password',None)
            username = request.POST.get('username',None)
            me = auth.authenticate(request, email=email, password=password, username=username) #email과 password가 일치하는지 검사
            if me is not None: #사용자가 있는지 없는지만 구분 -> 만약있다고 하면 me에 그 사용자 넣어줌. 따라서 로그인 시켜줌
                auth.login(request, me)
                return redirect('/')
            else:
                return render(request, 'user/sign-in.html', {'error': '회원정보가 일치하지 않습니다 ;( '}) # html과 작업해야 함.


@login_required
def logout(request):
    auth.logout(request) # 인증되어있는 정보를 없애기
    return redirect("/")


def user_view(request):
    if request.method == 'GET': 
        user = request.user.is_authenticated # 사용자가 로그인 되어있는지 먼저 확인
        user_rating_list = Rating.objects.filter(user_id=request.user.id) 
        if user: 
            return render(request, 'user/user.html', {"user_rating_list": user_rating_list})

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            """
            현재 유저의 프로필을 가져오고
            받은 값으로 프로필을 갱신한다.
            """
            old_profile = request.user.profile
            old_profile.username = form.cleaned_data['username']
            old_profile.email = form.cleaned_data['email']
            old_profile.save()
            return redirect('/user')
    elif request.method == "GET":
        form = ProfileForm(instance=request.user.profile)
        return render(request, 'user/user.html', {
            'form': form,
        })
    # if request.method == 'POST':
    #     form = CustomUserChangeForm(request.POST, instance=request.user)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('articles:index')
    # else:
    #     form = CustomUserChangeForm(instance=request.user)
    # context = {
    #     'form': form
    # }
    # return render(request, 'user/user.html', context)


@login_required
def delete_user(request):
    user = UserModel(request, id)
    user.delete()
    return render(request, 'user/sign-in.html')

    # if request.method == 'POST':
    #     username=get_user_model().objects.get(username=request.POST)
    #     new_username=request.POST.get('username',None)
        
        
    #    # if username is not None:
            

    #   #  <int:username>

            
    #      #   return render(request, )
    #   #  else:
    #    #     return redirect(('/sign-in'))
    # else:
    #     return redirect('/')
