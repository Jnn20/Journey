from django.urls import path
from . import views

urlpatterns = [
    path('articles-by-category/<str:category>', views.ArticleListView.as_view(), name='articles-by-category'),
    path('articles-list/', views.ArticleListView.as_view(), name='article-list-page'),
    path('detials/<article_id>', views.article_detail, name='article-detail-page'),
    path('add-to-favorites', views.add_to_favorite, name='add-to-favorites'),
    path('remove-from-favorites', views.remove_from_favorite, name='remove-from-favorites'),
]

