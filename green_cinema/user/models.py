from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
import re
from difflib import SequenceMatcher
from django.core.exceptions import FieldDoesNotExist, ValidationError
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager



class UserProfileManager(BaseUserManager):
    """ Manager for user profiles """
    def create_user(self, email, password=None, username=None):
        """ Create a new user profile """
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email)
        username = self.model.normalize_username(username)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """ Create a new superuser profile """
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


# AbstractUser는 장고가 제공하는 기본적인 auth_user라는 table이랑 연동되는 class
class UserModel(AbstractUser, AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]
    
    class Meta:
        db_table = "user"



    # deleted_at에 삭제 요청받은 시간 저장.
    is_deleted = models.BooleanField(default=False, verbose_name='delete or not')
    # 데이터의 생성, 업데이트, 삭제시간 기록용
    deleted_at = models.DateTimeField(null=True)

    def delete(self, using=None, keep_parent=False):
        self.is_deleted = True
        self.deleted_at = datetime.now()
        self.save()

    def __str__(self):
     return self.email


# def passwordcheck(password):
#     if len(password) < 8 or len(password) > 21 and not re.findall('[0-9]+', password) and not \
#     re.findall('[a-z]+', password) or not re.findall('[A-Z]+', password):
#         print('비밀번호 기준(숫자, 영문 대소문자 구성)에 맞지 않습니다;)')
#         return False

#     elif not re.findall('[`~!@#$%^&*(),<.>/?]+', password):
#     # elif re.search('[`~!@#$%^&*(),<.>]'+, password) is None:
#         print('비밀번호는 최소 1개 이상의 특수문자가 포함되어야 합니다 ;)')
#         return False

#     print('비밀번호 입력이 완료되었습니다.')
#     return True
