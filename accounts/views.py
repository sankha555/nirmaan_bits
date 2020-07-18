from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from accounts.models import Volunteer, Visitor
from initiatives.models import Initiative
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
        volunteer = Volunteer.objects.filter(user = request.user)[0]
        if volunteer.is_pl:
            project = volunteer.project

            messages.success(request, 'Welcome ' + volunteer.name + ', Project Leader of ' + project.name)
            
            context = {
                'volunteers' : Volunteer.objects.filter(project = project),
                'project' : project
            }

            return render(request, 'initiatives/pl_dashboard.htm', context)

        else:
            messages.error(request, 'You are not authorized to access this page!')
            return redirect('index')
    else:
        messages.error(request, 'Your account was not verified as a Nirmaan Volunteer Account. Please check your email.')
        logout(request)
        return redirect('login')
        
'''
    CAN ONLY BE UPDATED ON RECIEPT OF EXCEL FILE
@login_required
def update_volunteers(request):

    file = #file_path of excel file containing all volunteers' details
    
    if request.user.is_superuser:
        projects = Initiative.objects.all()

        for project in projects:
           
    else:
        messages.error(request, 'You are not authorized to access this page!')
        return redirect('index')
'''   

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

def profile(request):
     if Volunteer.objects.filter(user = request.user).exists():       
        volunteer = Volunteer.objects.filter(user = request.user)[0]
        project = volunteer.project
        
        context = {
            'volunteer' : volunteer
            'project' : project
        }

        return render(request, 'initiatives/profile.htm', context)

    else:
        messages.error(request, 'You are not authorized to access this page!')
        return redirect('index')
    






# Create your views here.
