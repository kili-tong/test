import re

from django import forms
# from django_redis import get_redis_connection

from .models import User
# from verification.constants import SMS_CODE_LENGTH


class RegisterForm(forms.Form):
    userid = forms.CharField(max_length=120,
                               min_length=6,
                               required=True,
                               error_messages={'required': "id不能为空"})
    username = forms.CharField(max_length=120,
                               min_length=6,
                               required=True,
                               error_messages={'required': "用户名不能为空"})
    email = forms.EmailField(required=True,
                             error_messages={'required': "邮箱不能为空"})
    password = forms.CharField(max_length=120,
                               min_length=6,
                               required=True,
                               error_messages={'required':  "密码不能为空"})
