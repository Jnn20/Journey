from operator import attrgetter
from braces.views import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from profile_module.forms import EditProfileModelForm, EditUserModelForm
from profile_module.models import Profile
from post_module.models import Post, PostComments
from user_module.models import Contact
from article_module.models import ArticleComments
from user_module.models import User


# for profile directory
def user_info(request, slug):
    if slug is not None:
        user: User = get_object_or_404(User, is_active=True, username=slug)
        if user:
            following_count = user.following.count()
            followers_count = user.followers.count()
            context = {'user': user, 'following_count': following_count, 'followers_count': followers_count}
            return render(request, 'profile/user-info.html', context)
        else:
            raise Http404
    return render(request, 'profile/user-info.html', {'error': 'not found'})


@login_required()
def edit_profile(request):
    # get the instances
    current_user: User = User.objects.get(id=request.user.id)
    current_user_profile = Profile.objects.filter(user_id=current_user.id).first()
    # display form
    user_form = EditUserModelForm(instance=current_user)
    profile_form = EditProfileModelForm(instance=current_user_profile)
    # save the forms
    if request.method == 'POST':
        user_form = EditUserModelForm(request.POST,instance=current_user)
        profile_form = EditProfileModelForm(request.POST, request.FILES, instance=current_user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user-info', slug=current_user.username)
        else:
            messages.success(request, 'please enter allowed information')
    return render(request, 'profile/edit-profile.html', {'profile_form': profile_form, 'user_form': user_form})


def recent_activities(request, pk):
    # todo : add likes and posts
    user: User = User.objects.get(username=pk)
    comments = ArticleComments.objects.filter(user_id=user.id).all()
    following = Contact.objects.filter(user_from=user.id).all()
    all_activities = sorted([*comments, *following], key=attrgetter('created'), reverse=True)
    context = {'user': user, 'comments': comments, 'following': following, 'all_activities': all_activities}
    return render(request, 'profile/recent-activities.html', context)


class UserPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'profile/user-posts.html'
    paginate_by = 3

    def get_queryset(self):
        query = super().get_queryset()
        request = self.request
        query = query.filter(user_id=request.user.id).order_by('-publish')
        return query


@login_required
def favorites(request):
    user_profile = get_object_or_404(Profile, user_id=request.user.id)
    favorite_articles = user_profile.saved_articles.all()
    return render(request, 'profile/user-favorites.html', {'favorite_articles': favorite_articles})


class UserPostCommentsView(LoginRequiredMixin, ListView):
    model = PostComments
    template_name = 'profile/user-post-comments.html'
    paginate_by = 3

    def get_queryset(self):
        query = super().get_queryset()
        request = self.request
        query = query.filter(post__user=request.user.id)
        return query


# for user-contact directory
@login_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('user_id')
    if user_id is not None:
        user: User = User.objects.get(is_active=True, id=user_id)
        if user:
            if request.user in user.followers.all():
                Contact.objects.get(user_from=request.user, user_to=user).delete()
                follow = False
            else:
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                follow = True
            following_count = user.following.count()
            followers_count = user.followers.count()
            return JsonResponse({'follow': follow, 'following_count': following_count, 'followers_count': followers_count})
    else:
        return JsonResponse({'error': 'invalid user'})


def display_followers(request, username):
    user = User.objects.get(username=username, is_active=True)
    followers_obj = Contact.objects.filter(user_to_id=user.id).all()
    followers = []
    for follower in followers_obj:
        followers.append(follower.user_from)
    return render(request, 'user-contacts/user-followers.html', {'followers': followers, 'username': user.username})


def display_following(request, username):
    user = User.objects.get(username=username, is_active=True)
    following_obj = Contact.objects.filter(user_from_id=user.id).all()
    followings = []
    for following in following_obj:
        followings.append(following.user_to)
    return render(request, 'user-contacts/user-following.html', {'followings': followings, 'username': user.username})


# for staff directory
def staff_page(request):
    if not request.user.is_staff:
        raise Http404
    return render(request, 'staff/staff-page.html')
