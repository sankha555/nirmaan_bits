from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import Volunteer, Visitor
from initiatives.models import Initiative
from accounts.forms import VisitorRegistrationForm, ProfileForm
import xlrd
import datetime

@login_required
def volunteer_login_validation(request):
    email = request.user.email
    print(email)
    if Volunteer.objects.filter(user = request.user).exists():
        messages.success(request, 'Welcome, ' + request.user.volunteer.name + '!')
        return redirect('internal_index')
    elif Volunteer.objects.filter(bits_email = email).exists():
        volunteer = Volunteer.objects.get(bits_email = email)
        volunteer.user = request.user
        volunteer.save()
        messages.success(request, 'Welcome, ' + volunteer.name + '!')
        return redirect('internal_index')
    elif request.user.is_superuser:
        messages.success(request, 'Welcome, Administrator!')
        return redirect('internal_index')
    else:
        messages.error(request, 'Your account was not verified as a Nirmaan Volunteer Account. Please check your email.')
        logout(request)
        User.objects.get(email = email).delete()
        return redirect('login')

@login_required
def pl_dashboard(request):
    if Volunteer.objects.filter(user = request.user).exists():       
        volunteer = Volunteer.objects.filter(user = request.user)[0]
        if volunteer.is_pl:
            project = volunteer.project

            messages.success(request, 'Welcome ' + volunteer.name + ', Project Leader of ' + project.name)
            
            context = {
                'volunteers' : Volunteer.objects.filter(project = project).order_by('-is_pl','-year'),
                'project' : project
            }

            return render(request, 'initiatives/pl_volunteers.htm', context)

        else:
            messages.error(request, 'You are not authorized to access that page!')
            return redirect('internal_index')
    else:
        messages.error(request, 'Your account was not verified as a Nirmaan Volunteer Account. Please check your email.')
        logout(request)
        return redirect('login')  

def register_visitor(request):
    if request.method == "POST":
        form = VisitorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, 'Thanks for filling out our guestbook! You can now recieve updates about Nirmaan through email.')
            return redirect('internal_index')
        
    else:
        form = VisitorRegistrationForm()

    return render(request, 'initiatives/contact_form.htm', {'form' : form})

@login_required
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
        messages.error(request, 'You are not authorized to access that page!')
        return redirect('internal_index')

        
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

        return redirect('internal_index')
           
    else:
        messages.error(request, 'You are not authorized to access that page!')
        return redirect('internal_index')




# Create your views here.
