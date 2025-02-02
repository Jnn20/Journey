from django.urls import path
from article_module.views import delete_article, AllArticlesView, EditArticleView, \
    DisplayCommentsView, NewArticleView
from post_module.views import PostsSettingView
from user_module.views import UsersSettingView
from . import views


urlpatterns = [
    # for profile directory
    path('user-info/<slug>', views.user_info, name='user-info'),
    path('edit-profile/', views.edit_profile, name='edit-profile-page'),
    path('user-posts/', views.UserPostsView.as_view(), name='user-posts-page'),
    path('user-post-comments/', views.UserPostCommentsView.as_view(), name='user-post-comments-page'),
    path('user-favorites/', views.favorites, name='user-favorites-page'),
    path('recent-activities/<pk>', views.recent_activities, name='recent-activities-page'),

    # for staff directory
    path('staff', views.staff_page, name='staff-page'),
    path('all-articles', AllArticlesView.as_view(), name='articles-page'),
    path('new-article', NewArticleView.as_view(), name='new-article-page'),
    path('edit-article/<pk>', EditArticleView.as_view(), name='edit-article-page'),
    path('delete-article/<pk>', delete_article, name='delete-article'),
    path('display-comments/<pk>', DisplayCommentsView.as_view(), name='display-comments-page'),
    path('users-setting/', UsersSettingView.as_view(), name='users-setting-page'),
    path('posts-setting/', PostsSettingView.as_view(), name='posts-setting-page'),

    # for user-contacts directory
    path('follow/', views.user_follow, name='follow'),
    path('followers/<username>', views.display_followers, name='display-followers-page'),
    path('following/<username>', views.display_following, name='display-following-page'),
]
