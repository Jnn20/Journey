from django.views.generic import FormView
from utils.email_services import send_email
from .forms import ContactUsForm


class ContactUsView(FormView):
    template_name = 'contact-us.html'
    form_class = ContactUsForm
    success_url = '/contact-us/'

    def form_valid(self, form):
        # sending an email from "site email" to the "admin email" contains of user's info.
        send_email(form.cleaned_data['subject'],
                   {'email': self.request.user.email,
                    'message': form.cleaned_data['message'],
                    'name': form.cleaned_data['name']},
                   'email_messages/user-contact-message.html',
                   'lunathecoolgurl@gmail.com')
        return super().form_valid(form)
