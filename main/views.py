from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from .models import ContactSender
from .forms import ContactForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


def index(request):
    return render(request, "initiatives/index.html")

def about(request):
    return render(request, "initiatives/index.html")

def contact(request):
    return render(request, "initiatives/index2.html")


def password_reset(request):

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password for Administrator Changed Successfully!', fail_silently=False)
            return redirect('home')
    
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'initiatives/password_reset.html', {'form': form})


def internal_index(request):
    return render(request, "initiatives/index3.html")




