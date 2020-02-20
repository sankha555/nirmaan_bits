from django import forms
from .models import ContactSender


class ContactForm(forms.ModelForm):

    class Meta:
        model = ContactSender
        fields = ['name', 'phone', 'address', 'message']

