from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from journey import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home_module.urls')),
    path('', include('about_module.urls')),
    path('', include('user_module.urls')),
    path('', include('article_module.urls')),
    path('', include('contact_module.urls')),
    path('', include('profile_module.urls')),
    path('', include('post_module.urls')),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
