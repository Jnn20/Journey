from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control'}),
        validators=[validators.MaxLengthValidator(50)],
    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ''}),
        validators=[validators.MaxLengthValidator(100), validators.EmailValidator]
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': '', 'class': 'form-control'}),
        validators=[validators.MaxLengthValidator(50)]
    )
    confirm_password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ''}),
        validators=[validators.MaxLengthValidator(50)]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        else:
            raise ValidationError('password and the double check are not the same.')


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ''}),
        validators=[validators.MaxLengthValidator(100), validators.EmailValidator]
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': '', 'class': 'form-control'}),
        validators=[validators.MaxLengthValidator(50)]
    )


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={'placeholder': '', 'class': 'form-control'}),
        validators=[validators.MaxLengthValidator(100), validators.EmailValidator]
    )


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': '', 'class': 'form-control'}),
        validators=[validators.MaxLengthValidator(50)]
    )
    confirm_password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ''}),
        validators=[validators.MaxLengthValidator(50)]
    )

    def clean_confirm_password(self):
        user_pass = self.cleaned_data.get('password')
        user_confirm_pass = self.cleaned_data.get('confirm_password')

        if user_pass == user_confirm_pass:
            return user_confirm_pass
        else:
            raise ValidationError('password and the double enter are not the same')
