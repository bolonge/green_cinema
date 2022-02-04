from hashlib import new
from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model #사용자가 데이터베이스 안에 있는지 검사하는 함수
from django.contrib import auth
from django.contrib.auth.decorators import login_required
        


def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/sign-up.html')
    elif request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)

        if password != password2:
            return render(request, 'user/sign-up.html')
        
        else:

            old_user = get_user_model().objects.filter(email=email)
            # old_user = UserModel.objects.filter() ## .filter()는 데이터가 있으나 없으나 에러를 발생하지 않음. 데이터가 있으면 검색해서 가져오고 없으면 없다고 말해줌. but 위 get()은 데이터가 무조건 있어야함. 없으면 에러일어남
            if old_user:
                return render(request, 'user/sign-up.html')   # 이미 사용자 username이 있다면, signup 페이지로 다시 가게끔
            else:
                UserModel.objects.create_user(email=email, password=password)
                return redirect('/sign-in')

def sign_in_view(request):
    if request.method == 'POST':
        email = request.POST.get('email',None)
        password = request.POST.get('password',None)

        me = auth.authenticate(request, email=email, password=password) #email과 password가 일치하는지 검사
        if me is not None: #사용자가 있는지 없는지만 구분 -> 만약있다고 하면 me에 그 사용자 넣어줌. 따라서 로그인 시켜줌
            auth.login(request, me)
            return redirect('/')
        else:
            return redirect('/sign-in')
    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/sign-in.html')

def user_view(request):
    return render(request, 'user/user.html')
