from django import forms
from .models import ContactSender, Donation

class ContactForm(forms.ModelForm):

    class Meta:
        model = ContactSender
        fields = ['name', 'phone', 'address', 'message']


class DonationForm(forms.ModelForm):
    
    class Meta:
        model = Donation
        fields = ['donor_name', 'amount', 'message']
        
        