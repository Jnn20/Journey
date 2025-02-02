from django.db import models
from django.urls import reverse
from user_module.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='posts_pic', blank=True, null=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} by {self.user.username}'

    def get_absolute_url(self):
        return reverse('post-detail-page', args=[self.id])


class PostComments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='posted_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_comments')
    text = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return f'{self.user.username} left a comment for {self.post.title}'


class SavedPosts(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saved')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_posts')

    def __str__(self):
        return f'{self.user.username} saved {self.post.title}'

