from django.shortcuts import render, redirect
from .models import UserModel
from django.contrib.auth import get_user_model  # 사용자가 데이터베이스 안에 있는지 검사하는 함수
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from movie.models import Rating
from .forms import ProfileForm
# # email
# from django.core.mail import EmailMessage

# def send_email(request):
#     subject = "message"
#     to = ["rollypinl@gmail.com"]
#     from_email = "2022have12@gmail.com"
#     message = "메시지 테스트"
#     EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()


def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated  # 로그인 된 사용자가 요청하는 건지
        if user:  # 로그인 되어있다면
            return redirect('/')  # main page로 -> 우리는 index려나?
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

        elif UserModel.objects.filter(email=email).exists():
            return render(request, 'user/sign-up.html', {'error': '이미 사용하고 있는 이메일입니다 ;)'})
        else:
            exist_user = get_user_model().objects.filter(email=email)
            if exist_user:
                return render(request, 'user/sign-up.html', {'error': '이메일이 이미 존재합니다 ;( '})
            else:
                user = UserModel.objects.create_user(
                    email=email, password=password)
                user.username = username
                user.save()
                return redirect('/sign-in')  # 회원가입이 완료되었으므로 로그인 페이지로 이동


def sign_in_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated  # 사용자가 로그인 되어있는지 검사
        if user:
            return redirect('/')
        else:
            return render(request, 'user/sign-in.html')
    elif request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        username = request.POST.get('username', None)
        # email과 password가 일치하는지 검사
        exist_user = get_user_model().objects.filter(email=email)[0]
        if exist_user.is_deleted:
            return render(request, 'user/sign-in.html', {'error': '탈퇴한 계정입니다 ;( '})
        me = auth.authenticate(request, email=email,
                               password=password, username=username)
        if me is not None:  # 사용자가 있는지 없는지만 구분 -> 만약있다고 하면 me에 그 사용자 넣어줌. 따라서 로그인 시켜줌
            auth.login(request, me)
            return redirect('/')
        else:
            # html과 작업해야 함.
            return render(request, 'user/sign-in.html', {'error': '회원정보가 일치하지 않습니다 ;( '})


@login_required
def logout(request):
    auth.logout(request)  # 인증되어있는 정보를 없애기
    return redirect("/")


@login_required
def user_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            """
            현재 유저의 프로필을 가져오고
            받은 값으로 프로필을 갱신한다.
            """
            old_user = UserModel.objects.get(id=request.user.id)
            if old_user.email != form.cleaned_data["email"]:
                if UserModel.objects.filter(email=form.cleaned_data["email"]).exists():
                    return render(request, 'user/user.html', {'error': '이미 존재하는 이메일입니다 ;)'})

            else:
                old_user.email = form.cleaned_data["email"]
                old_user.username = form.cleaned_data["username"]
                old_user.save()

            # old_profile = UserModel.objects.get(id=request.user.id)
            # old_profile.username = form.cleaned_data['username']
            # old_profile.email = form.cleaned_data['email']
            # old_profile.save()

                return redirect('/user')

            # 원래 있는 정보들이면 실행(저장)이 안되게
            # username 이나 email 둘 중 하나만 수정해도 완료되게.

        else:
            return render(request, 'user/user.html', {'error': '이미 사용하는 이메일입니다 ;) '})

    elif request.method == 'GET':
        user = request.user.is_authenticated  # 사용자가 로그인 되어있는지 먼저 확인
        user_rating_list = Rating.objects.filter(user_id=request.user.id)
        form = ProfileForm()
        if user:
            return render(request, 'user/user.html', {"user_rating_list": user_rating_list, "form": form})


@login_required
def delete_user(request):
    user = UserModel.objects.get(id=request.user.id)
    user.delete()
    auth.logout(request)
    return render(request, 'user/sign-in.html')
