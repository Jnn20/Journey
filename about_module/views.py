from django.views.generic import ListView, DetailView
from user_module.models import User


# display about page and staff's profile page
class AboutView(ListView):
    template_name = 'about.html'
    model = User
    ordering = 'username'
    context_object_name = 'staff_list'

    def get_queryset(self, **kwargs):
        query = super().get_queryset()
        query = query.filter(is_staff=True)
        print(query)
        return query
