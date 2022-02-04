from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
import re
from difflib import SequenceMatcher
from django.core.exceptions import FieldDoesNotExist, ValidationError


# AbstractUser는 장고가 제공하는 기본적인 auth_user라는 table이랑 연동되는 class
class UserModel(AbstractUser):
    class Meta:
        db_table = "user"
    # nick_name = models.CharField(max_length=45)
    # deleted_at에 삭제 요청받은 시간 저장.
    is_deleted = models.BooleanField(default=False, verbose_name='delete or not')
    # 데이터의 생성, 업데이트, 삭제시간 기록용
    deleted_at = models.DateTimeField(null=True)

    def delete(self, using=None, keep_parent=False):
        self.is_deleted = True
        self.deleted_at = datetime.now()
        self.save()


class UserAttributeSimilarityValidator:
    '''
    Validate whether the password is sufficiently different from the user’s
    attributes.
    If no specific attributes are provided, look at a sensible list of
    defaults. Attributes that don’t exist are ignored. Comparison is made to
    not only the full attribute value, but also its components, so that, for
    example, a password is validated against either part of an email address,
    as well as the full address.
    '''
    DEFAULT_USER_ATTRIBUTES = ('username', 'first_name', 'last_name', 'email')
    def __init__(self, user_attributes=DEFAULT_USER_ATTRIBUTES, max_similarity=0.7):
        self.user_attributes = user_attributes
        self.max_similarity = max_similarity
    def validate(self, password, user=None):
        if not user:
            return
        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= self.max_similarity:
                    try:
                        verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        ("The password is too similar to the %(verbose_name)s."),
                        code='password_too_similar',
                        params={'verbose_name': verbose_name},
                    )
    def get_help_text(self):
        return ('Your password can’t be too similar to your other personal information.')