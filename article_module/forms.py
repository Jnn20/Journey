from django import forms
from article_module.models import ArticleComments, Article


class CreateNewArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'city', 'reading_duration', 'categories', 'short_description', 'slug', 'text', 'image']


class EditArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'city', 'reading_duration', 'categories', 'short_description', 'slug', 'text', 'image']


class ArticleCommentModelForm(forms.ModelForm):
    class Meta:
        model = ArticleComments
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'class': 'form-control bg-transparent',
                                                 'placeholder': 'write your comment here...'})}

