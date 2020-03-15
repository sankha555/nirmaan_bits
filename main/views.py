from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from .models import ContactSender
from .forms import ContactForm


def index(request):
    return render(request, "initiatives/index.html")

def index2(request):
    return render(request, "initiatives/index2.html")

def about(request):
    return render(request, "initiatives/about.html")

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():

            sender = form.save(commit=False)
            sender.save()

            return redirect('home')
    else:
        form = ContactForm()

    return render(request, 'initiatives/contact_form.html', {'form': form})

# Create your views here.
