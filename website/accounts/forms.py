from django import forms
from .models import *
# from django.contrib.auth.models import User


error = {
    'required':'این فیلد اجباری است',
    'invalid':'ایمیل شما نا معتبر است'
}

class UserRegisterForm(forms.Form):
    user_name = forms.CharField(max_length=100,error_messages=error, widget=forms.TextInput(attrs={'placeholder':'نام کاربری'}))
    email = forms.EmailField(error_messages=error,widget=forms.EmailInput(attrs={'placeholder':'ایمیل'}))
    first_name = forms.CharField(max_length=50,error_messages=error,widget=forms.TextInput(attrs={'placeholder':'نام'}))
    last_name = forms.CharField(max_length=50,error_messages=error,widget=forms.TextInput(attrs={'placeholder':'نام نام خانوادگی'}))
    password_1 = forms.CharField(max_length=50,error_messages=error,widget=forms.PasswordInput(attrs={'placeholder':'پسورد'}))
    password_2 = forms.CharField(max_length=50,error_messages=error,widget=forms.PasswordInput(attrs={'placeholder':'تکرار پسورد'}))



    def clean_user_name(self):
        user = self.cleaned_data['user_name']
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError('USER EXIST :)')
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('DUPLICATE EMAIL<3')
        return email

    def clean_password_2(self):
        password1 = self.cleaned_data['password_1']
        password2 = self.cleaned_data['password_2']
        if password1 != password2:
            raise forms.ValidationError('password not sameeeeeeeee')

        elif len(password2) < 8 :
            raise forms.ValidationError('PASS IS SHORT!!!!!!')

        elif not any (x.isupper() for x in password2):
            raise forms.ValidationError('ATLEAST USER ONE BIG LETTER')
        return password1

class UserLoginForm(forms.Form):
    user = forms.CharField( widget=forms.TextInput(attrs={'placeholder':'نام کاربری'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'پسورد'}))


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','first_name','last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone','address']

class PhoneForm(forms.Form):
    phone = forms.IntegerField()

class CodeForm(forms.Form):
    code = forms.IntegerField()