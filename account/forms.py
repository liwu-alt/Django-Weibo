from django import forms
from django.forms import widgets
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", widget=forms.TextInput(attrs={"class": "form-control"})),
    password = forms.CharField(label="密  码", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='密        码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='再次输入密码', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError(r"两次密码不相同")
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('sex', 'birth', 'profile', 'icon', )
        labels = {
            'sex': '性别',
            'birth': '出生日期',
            'profile': '个人简介',
            'icon': '头像',
        }