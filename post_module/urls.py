from django.urls import path
from post_module import views

urlpatterns = [
    # for "posts" directory
    path('post-detail/<pk>', views.PostDetailView.as_view(), name='post-detail-page'),
    path('create-post/', views.CreatePostView.as_view(), name='create-post-page'),
    path('edit-post/<pk>', views.EditPostView.as_view(), name='edit-post-page'),
    path('delete-post/', views.delete_post, name='delete-post'),
    path('like-post', views.like_post, name='like-post'),

    # for "community" directory
    path('explore', views.ExploreView.as_view(), name='explore-page'),
    path('user-following-posts', views.FollowingPostsView.as_view(), name='user-following-posts-page'),

]
