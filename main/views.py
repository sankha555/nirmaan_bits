from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from .models import ContactSender, Donation
from .forms import ContactForm, DonationForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from initiatives.models import Initiative
from accounts.models import Volunteer
from accounts.forms import VisitorRegistrationForm
import random
import json


# Razorpay
import razorpay
client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))
#client.set_app_details({"title" : "Nirmaan Organization BITS Pilani", "version" : "1"})

def to_paise(amount):
    return float(amount*100)

def index(request):
    #return render(request, "initiatives/index2.htm")
    return redirect('internal_index')

def about(request):
    if request.method == "POST":
        form = VisitorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('about')
    else:
        form = VisitorRegistrationForm()

    return render(request, 'initiatives/about.htm', {'form':form})

#def contact(request):
#    return render(request, "initiatives/index2.htm")

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
    return render(request, 'initiatives/password_reset.htm', {'form': form})


def internal_index(request):
    return render(request, "initiatives/index3.htm")

def main_contacts(request):
    return render(request, "initiatives/main_contacts.htm")

def donations(request):
    return render(request, "initiatives/donations.htm")

def test_index(request):
    return render(request, "initiatives/index2.htm")

def troubleshooting(request):
    return render(request, "initiatives/troubleshooting.htm")

def donations(request):
    
    
    if request.method=="POST":
        
        form = DonationForm(request.POST)
        if form.is_valid():
            
            form.save()
            donation = form.instance
            
            context = {
                "amount" : float(donation.amount),
                "currency" : 'INR',
                "receipt" : ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))+'#'+str(donation.donor_name.replace(' ', '-'))+"_DonationID_"+str(donation.id)+"_on_"+str(donation.date),
                "notes" : {'donation_id':donation.id},
                "payment_capture":'0',
            }
            
            resp = client.order.create(data=context)
        
    else:
        form = DonationForm()
        
    return render(request, "initiatives/donations.htm")