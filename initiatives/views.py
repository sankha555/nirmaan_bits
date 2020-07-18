from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.http import HttpResponseRedirect
from .models import Initiative, InitiativeComment
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CommentForm, InitiativeCreateForm, InitiativeUpdateForm
from django.conf import settings
from django.contrib import messages


def home(request):

    inits = Initiative.objects.all().order_by('-date_started')
    context = {'inits':inits}
    return render(request, 'initiatives/home.htm', context)

def dash(request):
    return render(request, 'initiatives/dash.htm')


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

@staff_member_required
def update_initiative(request, pk):

    init = get_object_or_404(Initiative, pk=pk)
    if request.method == 'POST':
        form = InitiativeUpdateForm(
            request.POST, request.FILES, instance=init)

        if form.is_valid():
            init.save()
            messages.info(request, 'Initiative "%s" updated successfully!' % init.name, fail_silently=True)

            return redirect('init_detail', pk=init.id)
    else:
        form = InitiativeUpdateForm()

    return render(request, 'initiatives/initiative_form.htm', {'form': form})


class InitiativeDeleteView(LoginRequiredMixin, DeleteView, SuccessMessageMixin):
    model = Initiative
    success_url = '/initiatives'
    context_object_name = 'init'
    success_message = "Initiative %(name)s was deleted"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, init_name=self.object.name)


def init_detail(request, pk):
    initiative = get_object_or_404(Initiative, pk=pk)
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.initiative = initiative
            comment.save()
            return redirect('init_detail', pk=initiative.pk)
    else:
        form = CommentForm()

    return render(request, 'initiatives/init_detail.htm', {'form':form, 'init':initiative})

def like_initiative(request, pk):
    initiative = get_object_or_404(Initiative, pk=pk)

    initiative.likes += 1
    initiative.save()
    
    return redirect('init_detail', pk=initiative.id)


