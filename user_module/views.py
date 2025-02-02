from braces.views import StaffuserRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View
from user_module.forms import RegisterForm, LoginForm, ForgetPasswordForm, ResetPasswordForm
from user_module.models import User
from django.contrib.auth import login, logout
from utils.email_services import send_email


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = register_form.cleaned_data.get('username')
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            user: bool = User.objects.filter(email__iexact=user_email).exists()
            if user:
                register_form.add_error('email', 'this email is already exists as an account.')
            else:
                new_user = User(username=user_name, email=user_email, email_active_code=get_random_string(72),
                                is_active=False)
                new_user.set_password(user_password)
                new_user.save()

                # email part
                subject = 'you have created an account in Journey'
                context = {'username': new_user.username, 'code': new_user.email_active_code}
                send_email(subject, context, 'email_messages/register-code-message.html', new_user.email)

                return redirect(reverse('home-page'))
        return render(request, 'register.html', {'register_form': register_form})


class ActivateAccountView(View):
    def get(self, request, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                return redirect(reverse('register-page'))
        else:
            raise Http404


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'login.html', {'login_form': login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_password = login_form.cleaned_data.get('password')
            user_email = login_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user:
                if user.is_active:
                    check_pass = user.check_password(user_password)
                    if check_pass:
                        login(request, user)
                        return redirect('home-page')
                    else:
                        login_form.add_error('email', 'email or password is wrong')
                else:
                    login_form.add_error('email', 'your account is not active')
            else:
                login_form.add_error('email', 'no user has found')

        return render(request, 'login.html', {'login_form': login_form})


class ForgetPasswordView(View):
    def get(self, request):
        forget_password_form = ForgetPasswordForm()
        return render(request, 'forget-password.html', {'forget_password_form': forget_password_form})

    def post(self, request):
        forget_password_form = ForgetPasswordForm(request.POST)
        if forget_password_form.is_valid():
            user_email = forget_password_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()

            if user:
                # email part
                subject = 'you have requested for changing your password in Journey'
                context = {'username': user.username, 'code': user.email_active_code}
                send_email(subject, context, 'email_messages/forget-password-message.html', user.email)

                return redirect(reverse('home-page'))
            else:
                forget_password_form.add_error('email', 'no account has found')
        return render(request, 'forget-password.html', {'forget_password_form': forget_password_form})


class ResetPasswordView(View):
    def get(self, request, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('login-page'))
        else:
            reset_password_form = ResetPasswordForm(request.POST)
            return render(request, 'reset-password.html', {'reset_password_form': reset_password_form, 'user': user})

    def post(self, request, active_code):
        reset_password_form = ResetPasswordForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if reset_password_form.is_valid():
            if user is None:
                return redirect(reverse('login-page'))
            user_pass = reset_password_form.cleaned_data.get('confirm_password')
            user.set_password(user_pass)
            user.email_active_code = get_random_string(72)
            user.is_active = True  # the user can activate her/his account
            user.save()
            return redirect(reverse('login-page'))

        return render(request, 'reset-password.html', {'reset_password_form': reset_password_form, 'user': user})


class LogoutView(View):
    def get(self, request):
        current_user: User = request.user.username
        return render(request, 'logout.html', {'current_user': current_user})

    def post(self, request):
        logout(request)
        return redirect(reverse('home-page'))


class UsersSettingView(StaffuserRequiredMixin, View):  # usage : profile_module / in staff part
    def get(self, request):
        users = User.objects.filter(is_staff=False, is_superuser=False)
        return render(request, 'staff/users-setting.html', {'users': users})

    def post(self, request):
        checkbox_input = request.POST.keys()  # get info from the checkbox (contains of checked boxes & token)
        user_ids = [int(user_id) for user_id in checkbox_input if user_id.isdigit()]  # filter all checked IDs
        users = User.objects.filter(is_staff=False, is_superuser=False)

        for user in users:
            if user.id in user_ids:
                user.is_active = True
                user.save()
            else:
                user.is_active = False
                user.save()
        return render(request, 'staff/users-setting.html', {'users': users})

