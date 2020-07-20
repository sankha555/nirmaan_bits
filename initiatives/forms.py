from django import forms
from .models import InitiativeComment, Initiative

class InitiativeCreateForm(forms.ModelForm):

    class Meta:
        model = Initiative
        fields = ['name', 'description', 'date_started', 'banner_image', 'volunteers_file']

class InitiativeUpdateForm(forms.ModelForm):

    class Meta:
        model = Initiative
        fields = ['description', 'banner_image', 'volunteers_file']
    

class CommentForm(forms.ModelForm):

    class Meta:
        model = InitiativeComment
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }



