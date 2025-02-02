from django.shortcuts import render
from django.views.generic import TemplateView
from article_module.models import Article


class HomeView(TemplateView):
    template_name = 'home.html'


def header_component(request):
    return render(request, 'header-component.html')


def footer_component(request):
    return render(request, 'footer-component.html')


def search(request):  # search for articles by their title name
    results = []  # query = None
    if 'query' in request.GET:  # query = not None
        query = request.GET.get('query')
        results: Article = Article.objects.filter(is_active=True, title__icontains=query).all()
    return render(request, 'search-results.html', {'results': results})

