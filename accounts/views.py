from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from accounts.models import Volunteer, Visitor
from initiatives.models import Initiative
from accounts.forms import VisitorRegistrationForm, ProfileForm
import xlrd
import datetime

@login_required
def volunteer_login_validation(request):

    if Volunteer.objects.filter(user = request.user).exists() or request.user.is_superuser:       
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

            return render(request, 'initiatives/pl_volunteers.htm', context)

        else:
            messages.error(request, 'You are not authorized to access this page!')
            return redirect('index')
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

def profile(request):
    if Volunteer.objects.filter(user = request.user).exists():       
        volunteer = Volunteer.objects.filter(user = request.user)[0]
        project = volunteer.project

        if request.method == "POST":
            form = ProfileForm(request.POST, request.FILES, instance = volunteer)
            
            if form.is_valid():
                form.save()
                return redirect('profile')

        else:
            form = ProfileForm(instance = volunteer)

        context = {
            'volunteer' : volunteer,
            'project' : project,
            'form' : form
        }

        return render(request, 'initiatives/profile.htm', context)

    else:
        messages.error(request, 'You are not authorized to access this page!')
        return redirect('index')

        
@login_required
def update_volunteers(request):
    
    if request.user.is_superuser:
        projects = Initiative.objects.all()

        for project in projects:
            file = project.volunteers_file
            wb = xlrd.open_workbook(file.path)
            sheet = wb.sheet_by_index(0)
            sheet.cell_value(0, 0)

            rows = sheet.nrows
            cols = sheet.ncols

            for i in range(1, rows):
                if sheet.cell_value(i, 0) == "" or sheet.cell_value(i, 0) == None:
                    continue
                
                try: 
                    volunteer = Volunteer.objects.get(bits_id = sheet.cell_value(i, 1))
                except:
                    volunteer = Volunteer.objects.create(
                        bits_id = sheet.cell_value(i, 1),
                    )
                
                volunteer.name = str(sheet.cell_value(i, 0)).title()
                phone = str(sheet.cell_value(i, 2))
                if phone[-2:] == ".0":
                    phone = phone[:-2]
                volunteer.phone = phone
                volunteer.bits_email = sheet.cell_value(i, 3)

                volunteer.project = project
                volunteer.year = (datetime.datetime.now().year - int(str(sheet.cell_value(i, 1))[0:4]) + 1) if datetime.datetime.now().month >= 8 else (datetime.datetime.now().year - int(str(sheet.cell_value(i, 1))[0:4]))
                volunteer.save()


        return redirect('index')
           
    else:
        messages.error(request, 'You are not authorized to access this page!')
        return redirect('index')




# Create your views here.
