from django import forms


class ContactUsForm(forms.Form):
    name = forms.CharField(label='', max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control form-floating col-md-6',
                                           'placeholder': 'Your Name'})
                           )
    subject = forms.CharField(label='', max_length=500, widget=forms.TextInput(attrs={'class': 'form-control form-floating col-md-6',
                                           'placeholder': 'The Subject'})
                              )
    message = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control form-floating col-md-6',
                                           'placeholder': 'Your Message'})
                              )
