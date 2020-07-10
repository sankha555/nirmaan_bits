from django.forms import forms
from accounts.models import Visitor

class VisitorRegistrationForm(forms.ModelForm):

    class Meta:
        model = Visitor
        fields = '__all__'