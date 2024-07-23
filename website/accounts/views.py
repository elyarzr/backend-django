from django.shortcuts import render, redirect, reverse
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from random import randint
import ghasedakpack
from django.core.mail import EmailMessage
from django.views import View
from django.utils.encoding import force_str,force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
import django
django.utils.encoding.force_text = force_str



class EmailToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.id) + text_type(timestamp))


email_generator = EmailToken()


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        # ایا فیلد هایی که وارد کرده تمیز(درست)هستند
        if form.is_valid():
            data = form.cleaned_data
            # با objects با مدل ها مون ارتباط داریم
            user = User.objects.create_user(username=data['user_name'], email=data['email'],
                                            first_name=data['first_name'],
                                            last_name=data['last_name'], password=data['password_2'])
            messages.success(request, 'register successfully')

            user.is_active = True
            user.save()

            domain = get_current_site(request).domain
            uid64 = urlsafe_base64_encode(force_bytes(user.id))
            url = reverse('accounts:active', kwargs={'uidb64': 'uidb64', 'token': email_generator.make_token(user)})
            link = 'http://' + domain + url

            #send email to user
            email = EmailMessage(
                'active user',
                link,
                'test<2elyarzarrabi80@gmail.com>',
                [data['email']],

            )
            email.send(fail_silently=False)
            messages.warning(request, 'کاربر محترم لطفا برای فعال سازی به ایمیل خود مراجعه کنید', 'warning')
            return redirect('home:home')
    else:
        form = UserRegisterForm()
    context = {'form': form}

    return render(request, 'accounts/register.html', context)


class RegisterEmail(View):
    def get(self, request,uidb64,token):
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        if user and email_generator.check_token(user,token):
            user.is_active = True
            user.save()
            return redirect('accounts:login')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = authenticate(request, username=User.objects.get(email=data['user']), password=data['password'])
            except:
                user = authenticate(request, username=data['user'], password=data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'welcom to my site', )
                return redirect('home:home')
            else:
                messages.error(request, 'user or password is wrong', 'danger')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successfully', 'success')
    return redirect('home:home')


@login_required(login_url='accounts:login')
def user_profile(request):
    profile = Profile.objects.get(user_id=request.user.id)
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required(login_url='accounts:login')
def user_update(request):
    if request.method == 'POST':

        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if user_form and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'update successfully', 'success')
            return redirect('accounts:profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'user_form': user_form, 'profile_form': profile_form}

    return render(request, 'accounts/update.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'password change successfully', 'success')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'password id wrong', 'danger')
            return redirect('accounts:change')

    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change.html', {'form': form})


def phone(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            global random_code, phone
            data = form.cleaned_data
            phone = f"0{data['phone']}"
            random_code = randint(100, 1000)

            sms = ghasedakpack.Ghasedak("dc65a2f6c6871bf3449f8d4d076a235e62fdfedc55eded33b141e6805a67db3a")
            sms.send({
                'message': random_code,
                'receptor': phone,
                'linenumber': "10008566"
            })
            return redirect('accounts:verify')
    else:
        form = PhoneForm()
    return render(request, 'accounts/phone.html', {'form': form})


def verify(request):
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            if random_code == form.cleaned_data['code']:
                profile = Profile.objects.get(phone=phone)
                user = User.objects.get(profile__id=profile.id)
                login(request, user)
                messages.success(request, 'hi user!!!')
                return redirect('home:home')
            else:
                messages.error(request, 'your code is wrong')
    else:
        form = CodeForm()
    return render(request, 'accounts/code.html', {'form': form})
