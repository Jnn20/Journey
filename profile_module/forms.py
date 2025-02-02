from django import forms
from profile_module.models import Profile
from post_module.models import Post
from user_module.models import User


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'telegram', 'instagram', 'linkedin', 'job', 'about']


class EditUserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'phone']



