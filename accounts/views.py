from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from accounts.models import Volunteer, Visitor
from accounts.forms import VisitorRegistrationForm

@login_required
def volunteer_login_validation(request):

    if Volunteer.objects.filter(user = request.user).exists():       
        return redirect('index')
    else:
        messages.error(request, 'Your account was not verified as a Nirmaan Volunteer Account. Please check your email.')
        logout(request)
        return redirect('login')

@login_required
def pl_dashboard(request):
    if Volunteer.objects.filter(user = request.user).exists():       
        pass
    else:
        messages.error(request, 'Your account was not verified as a Nirmaan Volunteer Account. Please check your email.')
        logout(request)
        return redirect('login')
    

def register_visitor(request):
    if request.method == "POST":
        form = VistorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, 'Thanks for filling out our guestbook! You can now recieve updates about Nirmaan through email.')
            return redirect('index')
        
    else:
        form = VistorRegistrationForm()

    return render(request, 'initiatives/register_visitor.htm', {'form' : form})



# Create your views here.
