from django import forms
from post_module.models import Post, PostComments


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image']


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image']


class PostCommentModelForm(forms.ModelForm):
    class Meta:
        model = PostComments
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'class': 'form-control bg-transparent',
                                                 'placeholder': 'write your comment here...'})}


