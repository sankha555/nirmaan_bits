from django import forms
from .models import ContactSender, Donation

class ContactForm(forms.ModelForm):

    class Meta:
        model = ContactSender
        fields = '__all__'

'''
class DonationForm(forms.Form):
    donor_name = forms.CharField("Name", max_length=50, required=True)
    donor_name = forms.EmailField("Email", required=False)
  '''      
    