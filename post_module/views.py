from datetime import datetime
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, TemplateView
from post_module.forms import EditPostForm, PostCommentModelForm, CreatePostForm
from post_module.models import Post, PostComments
from profile_module.models import Profile


class CreatePostView(LoginRequiredMixin, View):
    def get(self, request):
        create_post_form = CreatePostForm()
        return render(request, 'posts/components/create-post.html', {'create_post_form': create_post_form})

    def post(self, request):
        create_post_form = CreatePostForm(request.POST, request.FILES)
        if create_post_form.is_valid():
            new_post = create_post_form.save(commit=False)
            new_post.user_id = request.user.id
            new_post.save()
            return redirect(reverse('user-posts-page'))
        return render(request, 'posts/components/create-post.html', {'create_post_form': create_post_form})


class EditPostView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        form = EditPostForm(instance=post)
        return render(request, 'posts/edit-post.html', {'form': form, 'post': post})

    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        form = EditPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'your post has changed')
            return redirect(reverse('user-posts-page'))
        return render(request, 'posts/edit-post.html', {'form': form, 'post': post})


class PostDetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.is_delete:
            if not request.user.is_staff:
                raise Http404
        comment_form = PostCommentModelForm()

        # check if this profile has liked this post (like section)
        profile = get_object_or_404(Profile, id=request.user.user_profile.id)
        if profile.liked_posts.filter(id=post.id).exists():
            liked = True
        else:
            liked = False

        context = {'post': post, 'comment_form': comment_form, 'liked': liked}
        return render(request, 'posts/post-detail.html', context)

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        comment_form = PostCommentModelForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user_id = request.user.id
            new_comment.post_id = post.id
            new_comment.save()
            return HttpResponseRedirect(pk, 'post-detail-page')
        return render(request, 'posts/post-detail.html', {'post': post, 'comment_form': comment_form})


@login_required
def delete_post(request):
    input_id = request.POST.get('input_id')
    post: Post = Post.objects.get(id=input_id)
    if post:
        post.delete()
        return JsonResponse({'status': 'deleted'})
    else:
        return JsonResponse({'error': 'not deleted'})


@login_required
def like_post(request):
    post_id = request.POST.get('post_id')
    profile = get_object_or_404(Profile, id=request.user.user_profile.id)
    post = get_object_or_404(Post, id=post_id)
    if post in profile.liked_posts.filter(id=post.id).all():
        profile.liked_posts.remove(post)
        liked = False
        likes_count = post.liked_by.count()
        return JsonResponse({'status': liked, 'likes_count': likes_count})
    else:
        profile.liked_posts.add(post)
        liked = True
        likes_count = post.liked_by.count()
        return JsonResponse({'status': liked, 'likes_count': likes_count})


class ExploreView(TemplateView):
    template_name = 'community/explore.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        # getting the last week
        date = datetime.today()
        week = date.strftime("%V")
        month = date.strftime("%M")

        # each part of explore
        latest_post = Post.objects.filter(is_delete=False).order_by('-publish')[:3]
        week_most_liked_posts = Post.objects.filter(is_delete=False).annotate(like_count=-Count('liked_by')).order_by('like_count')[:3]
        week_most_comment_posts = Post.objects.filter(is_delete=False).annotate(comment_count=-Count('posted_comments')).order_by('comment_count')[:3]
        most_active_users = Profile.objects.filter(user__is_active=True).annotate(scores=Max('activity_score')).order_by('-scores')[:4]
        context['latest_post'] = latest_post
        context['week_most_liked_posts'] = week_most_liked_posts
        context['week_most_comment_posts'] = week_most_comment_posts
        context['most_active_users'] = most_active_users
        return context


class FollowingPostsView(LoginRequiredMixin, ListView):
    template_name = 'community/following-posts.html'
    model = Post
    context_object_name = 'user_following_posts'

    def get_queryset(self):
        # query = super().get_queryset()
        user = self.request.user
        user_following = user.following.all().values_list('id', flat=True)
        user_following_posts: Post = Post.objects.filter(user_id__in=user_following).all().order_by('-publish')
        query = user_following_posts
        return query


class PostsSettingView(StaffuserRequiredMixin, View):  # usage : profile_module / in staff part
    def get(self, request):
        posts = Post.objects.all()
        return render(request, '../../profile_module/templates/staff/posts-setting.html', {'posts': posts})

    def post(self, request):
        checkbox_input = self.request.POST.keys()  # get info from the checkbox (contains of checked boxes & token)
        post_ids = [int(post_id) for post_id in checkbox_input if post_id.isdigit()]  # filter all checked IDs
        posts = Post.objects.all()

        for post in posts:
            if post.id in post_ids:
                post.is_delete = True
                post.save()
            else:
                post.is_delete = False
                post.save()
        return render(request, '../../profile_module/templates/staff/posts-setting.html', {'posts': posts})
