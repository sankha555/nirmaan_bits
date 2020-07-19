from django import forms
from accounts.models import Visitor, Volunteer

class VisitorRegistrationForm(forms.ModelForm):

    class Meta:
        model = Visitor
        fields = '__all__'

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Volunteer
        fields = [ 'image' ]