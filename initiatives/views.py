from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.http import HttpResponseRedirect
from .models import Initiative, InitiativeComment
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CommentForm, InitiativeCreateForm, InitiativeUpdateForm
from django.conf import settings

#ADMIN_USER = User.objects.get(username = settings.ADMIN_USERNAME)

inits = Initiative.objects.all().order_by('-date_started')
context = { 
    'inits' : Initiative.objects.all()
}

def home(request):
    return render(request, 'initiatives/home.html', context)

@staff_member_required
def create_initiative(request):

    if request.method == 'POST':
        form = InitiativeCreateForm(request.POST, request.FILES)
        if form.is_valid():

            initiative = form.save(commit=False)
            #img = request.FILES.getlist('file_field')

            #initiative.banner_image = img
            initiative.save()

            return redirect('init_detail')
    else:
        form = InitiativeCreateForm()

    return render(request, 'initiatives/initiative_form.html', {'form': form})

@staff_member_required
def update_initiative(request, pk):

    if request.method == 'POST':
        form = InitiativeUpdateForm(request.POST, request.FILES)
        if form.is_valid():

            initiative = form.save(commit=False)
            img = request.FILES.getlist('file_field')

            initiative.banner_image = img
            initiative.save()

            return redirect('init_detail', pk=initiative.id)
    else:
        form = InitiativeUpdateForm()

    return render(request, 'initiatives/initiative_form.html', {'form': form})


class InitiativeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Initiative
    success_url = '/'
    context_object_name = 'init'

    def test_func(self):
        initiative = self.get_object()
        if self.request.user == ADMIN_USER:
            return True
        return False

class InitiativeDetailView(DetailView):
    model = Initiative
    template_name = 'initiatives/init_detail.html'
    context_object_name = 'init'

def add_comment(request, pk):
    initiative = get_object_or_404(Initiative, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.initiative = initiative
            comment.save()
            return redirect('init_detail', pk=initiative.pk)
    else:
        form = CommentForm(instance=initiative)

    return render(request, 'initiatives/add_comment.html', {'form':form, 'initiative':initiative})

def like_initiative(request, pk):
    initiative = get_object_or_404(Initiative, pk=pk)

    initiative.likes += 1
    initiative.save()
    
    return redirect('init_detail', pk=initiative.id)


