from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, FormView
from profile_module.models import Profile
from .forms import ArticleCommentModelForm, CreateNewArticleForm, EditArticleForm
from .models import Article, ArticleCategory, ArticleComments
from braces import views


class ArticleListView(ListView):
    template_name = 'article-list.html'
    model = Article

    def get_queryset(self):
        query = super(ArticleListView, self).get_queryset()
        category = self.kwargs.get('category')
        if category is not None:
            query = query.filter(is_active=True, categories__url_title__iexact=category)
        return query

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = self.kwargs.get('category')
        context['cat'] = category
        return context


def article_detail(request, article_id):
    # article details and comments (the GET part)
    article: Article = get_object_or_404(Article, id=article_id, is_active=True)
    display_true_comments = ArticleComments.objects.filter(display=True, article_id=article_id).all()
    comment_form = ArticleCommentModelForm()

    # comment form section (the POST part)
    if request.method == "POST":
        comment_form = ArticleCommentModelForm(request.POST)
        if comment_form.is_valid():
            new_comment: ArticleComments = comment_form.save(commit=False)
            new_comment.user_id = request.user.id
            new_comment.article_id = article_id
            new_comment.save()
            return HttpResponseRedirect(article_id, 'article-detail-page')
    context = {'article': article, 'comment_form': comment_form, 'display_true_comments': display_true_comments}
    return render(request, 'article-details.html', context)


# render a component in article-list-page and articles-by-category
def article_category_component(request):
    main_categories = ArticleCategory.objects.filter(is_active=True).order_by('title')
    return render(request, 'components/article-category-component.html', {'main_categories': main_categories})


@login_required
def add_to_favorite(request):
    article_id = request.POST.get('article_id')
    try:  # if profile and article do exist , then add that article in user profile's saved_articles
        profile = Profile.objects.get(user_id=request.user.id)
        article = Article.objects.get(id=article_id)
        profile.saved_articles.add(article)
        return JsonResponse({'success': 'the article has been added to your favorite list.'})
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'the profile does not exists.'})
    except Article.DoesNotExist:
        return JsonResponse({'error': 'the article does not exists.'})


@login_required
def remove_from_favorite(request):
    article_id = request.GET.get('article_id')
    try:
        profile = Profile.objects.get(user_id=request.user.id)
        article = Article.objects.get(id=article_id)
        profile.saved_articles.remove(article)
        return JsonResponse({'success': True})
    except:  # should I use DoesNotExist ?
        return JsonResponse({'success': False})


class NewArticleView(views.StaffuserRequiredMixin, FormView):  # usage : profile_module / in staff part
    form_class = CreateNewArticleForm
    template_name = 'staff/new-article.html'
    success_url = '/all-articles'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class AllArticlesView(views.StaffuserRequiredMixin, ListView):  # usage : profile_module / in staff part
    template_name = 'staff/all-articles.html'
    model = Article
    paginate_by = 3


class EditArticleView(views.StaffuserRequiredMixin, View):  # usage : profile_module / in staff part
    def get(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        form = EditArticleForm(instance=article)
        return render(request, 'staff/edit-article.html', {'form': form, 'article': article})

    def post(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        form = EditArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
        return render(request, 'staff/edit-article.html', {'form': form, 'article': article})


@staff_member_required
def delete_article(request, pk):  # usage : profile_module / in staff part
    article = get_object_or_404(Article, id=pk)
    article.delete()
    return redirect('articles-page')


class DisplayCommentsView(views.StaffuserRequiredMixin, View):  # usage : profile_module / in staff part
    def get(self, request, pk):
        comments = ArticleComments.objects.filter(article_id=pk)
        return render(request, 'staff/display-comments.html', {'comments': comments})

    def post(self, request, pk):
        comments = ArticleComments.objects.filter(article_id=pk)
        for comment in comments:
            display_list = request.POST.get(str(comment.id)) == 'on'  # a list of checked items
            comment.display = display_list  # if the item has checked , then set the item's display "True".
            comment.save()
        return render(request, 'staff/display-comments.html', {'comments': comments})

