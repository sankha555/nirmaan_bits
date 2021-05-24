from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.http import HttpResponseRedirect
from .models import Initiative, InitiativeComment
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.admin.views.decorators import staff_member_required
from .forms import InitiativeCreateForm, InitiativeUpdateForm
from accounts.forms import VisitorRegistrationForm
from django.conf import settings
from django.contrib import messages
from accounts.models import Volunteer, Visitor

def home(request):

    inits = Initiative.objects.all().order_by('-date_started')
    context = {'inits':inits}
    return render(request, 'initiatives/home.htm', context)

def all_visitors(request):
    visitors = Visitor.objects.all().order_by('-date')
    context = {'visitors':visitors}
    return render(request, 'initiatives/all_visitors.htm', context)

def delete_visitor(request, pk):
    visitor = get_object_or_404(Visitor, pk = pk)
    visitor.delete()
    return redirect('all_visitors')

def prd(request):
    if request.method == "POST":
        form = VisitorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('prd')
    else:
        form = VisitorRegistrationForm()

    return render(request, 'initiatives/prd.htm', {'form':form})

def prd_volunteers(request):
    volunteers = Volunteer.objects.filter(prd_member = True).order_by('-year')
    return render(request, 'initiatives/prd_volunteers.htm', {'volunteers':volunteers})
    
@staff_member_required
def create_initiative(request):

    if request.method == 'POST':
        form = InitiativeCreateForm(request.POST, request.FILES)
        if form.is_valid():

            initiative = form.save(commit=False)
            initiative.save()
            messages.success(request, 'New initiative "%s" created successfully!' % initiative.name, fail_silently=True)

            return redirect('init_detail', pk=initiative.id)
    else:
        form = InitiativeCreateForm()

    return render(request, 'initiatives/initiative_form.htm', {'form': form})

@login_required
def update_initiative(request, slug):
    project = get_object_or_404(Initiative, slug = slug)
    if request.user.is_superuser or (request.user.volunteer.project == project and request.user.volunteer.is_pl):
        init = get_object_or_404(Initiative, slug=slug)
        if request.method == 'POST':
            form = InitiativeUpdateForm(
                request.POST, request.FILES, instance=init)

            if form.is_valid():
                init.save()
                messages.info(request, 'Initiative "%s" updated successfully!' % init.name, fail_silently=True)

                return redirect('init_detail', slug=slug)
        else:
            form = InitiativeUpdateForm(instance=init)

        return render(request, 'initiatives/initiative_form.htm', {'form': form})
    else:
        messages.error(request, 'You are not authorized to access that page!')
        return redirect('internal_index')


class InitiativeDeleteView(LoginRequiredMixin, DeleteView, SuccessMessageMixin):
    model = Initiative
    success_url = '/initiatives'
    context_object_name = 'init'
    success_message = "Initiative %(name)s was deleted"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, init_name=self.object.name)


def init_detail(request, slug):
    initiative = get_object_or_404(Initiative, slug = slug)
    
    if request.method == "POST":
        form = VisitorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('init_detail', slug=slug)
    else:
        form = VisitorRegistrationForm()

    return render(request, 'initiatives/init_detail.htm', {'form':form, 'init':initiative})

def like_initiative(request, pk):
    initiative = get_object_or_404(Initiative, pk=pk)

    initiative.likes += 1
    initiative.save()
    
    return redirect('init_detail', pk=initiative.id)

def volunteers(request, slug):
    project = get_object_or_404(Initiative, slug = slug)
    volunteers = Volunteer.objects.filter(project = project).order_by('-is_pl', '-year')

    return render(request, 'initiatives/volunteers.htm', {'project':project, 'volunteers':volunteers})

