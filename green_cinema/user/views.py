from hashlib import new
from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model #사용자가 데이터베이스 안에 있는지 검사하는 함수
from django.contrib import auth
from django.contrib.auth.decorators import login_required

        


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
        username = request.POST.get('username', None)
        if email == '' or password == '' or username == '' :
            return render(request, 'user/sign-up.html', {'error': '빈칸을 채워주세요 :)'}, )
        else:
            exist_user = get_user_model().objects.filter(email=email)
            if exist_user:
                return render(request, 'user/sign-up.html', {'error': '이메일이 이미 존재합니다 ;( '})
            else:
                UserModel.objects.create_user(email=email, password=password, username=username)
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
            me = auth.authenticate(request, email=email, password=password) #email과 password가 일치하는지 검사
            if me is not None: #사용자가 있는지 없는지만 구분 -> 만약있다고 하면 me에 그 사용자 넣어줌. 따라서 로그인 시켜줌
                auth.login(request, me)
                return redirect('/')
            else:
                return render(request, 'user/sign-in.html', {'error': '회원정보가 일치하지 않습니다 ;( '}) # html과 작업해야 함.


def user_view(request):
    return render(request, 'user/user.html')
