from django import forms
from .models import ContactSender, Donation

class ContactForm(forms.ModelForm):

    class Meta:
        model = ContactSender
        fields = ['name', 'phone', 'address', 'message']

'''
class DonationForm(forms.Form):
    donor_name = forms.CharField("Name", max_length=50, required=True)
    donor_name = forms.EmailField("Email", required=False)
  '''      
    