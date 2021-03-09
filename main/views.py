from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from .models import ContactSender, Donation
from .forms import ContactForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from initiatives.models import Initiative
from accounts.models import Volunteer
from accounts.forms import VisitorRegistrationForm
import random
import json
from PIL import Image, ImageFont, ImageDraw 
import xlwt
from django.http import HttpResponse
from datetime import date, datetime

def read_file(request):
    with open('../media/29A67ED8BA36CF4CD6D00DCEE680F336.txt', 'r') as f:
        file_content = f.read()
    return HttpResponse(file_content, content_type="text/plain")

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

def donation_cert(request):
    
    if request.method=="POST":
        
        data = dict(request.POST)
        print(data)
            
        # Variables
        name_text = str(data["donor_name"]).replace('[', '').replace(']', '').replace("'", "")
        name_coords = (400, 400)
        background_url = "media/background.jpg"
        title_font = ImageFont.truetype('media/Redressed-Regular.ttf', 100)
        text_color = (237, 230, 211)
        
        my_image = Image.open(background_url)
        image_editable = ImageDraw.Draw(my_image)
        image_editable.text(name_coords, name_text, text_color,  font=title_font)
        
        response = HttpResponse(content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename='+name_text+' - Nirmaan Organization.jpg'

        my_image.save(response, "JPEG")
        return response
                
    return render(request, "initiatives/donation_cert.htm")

def mask_register(request):
    
    if request.method == "POST":
        
        form = ContactForm(request.POST)
        
        if form.is_valid():
            form.save()
            customer = form.instance
            
            return redirect('index')
        
    else:
        form = ContactForm()
        
    return render(request, 'initiatives/mask_register.htm', {'form':form})

@staff_member_required
def mask_sales(request):
    
    if not request.user.is_superuser:
        return redirect('index')
    
    customers = ContactSender.objects.all().filter(marked = False)
    
    if len(customers) > 0:
        
        today = date.today().strftime("%d%m%Y")
        
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = "attachment; filename=Sales_"+str(today)+".xlsx"

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("Sales_"+str(today))

        #Writing the headers
        row = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = [
            'Name', 'Email', 'Phone', 'Address', 'PIN Code', 'TYPE 1 Quantity', 'TYPE 1 Color', 'TYPE 2 Quantity', 'TYPE 2 Color', 'TYPE 2 String', 'Remarks'
        ]

        for col in range(len(columns)):
            ws.write(row, col, columns[col], font_style)
        
        #Writing Orders data to the sheet
        font_style = xlwt.XFStyle()
        
        for customer in customers:
            row += 1
            ws.write(row, 0, customer.name, font_style)
            ws.write(row, 1, customer.email, font_style)
            ws.write(row, 2, customer.phone, font_style)
            ws.write(row, 3, customer.address, font_style)
            ws.write(row, 4, customer.pincode, font_style)
            ws.write(row, 5, customer.type1_quant, font_style)
            ws.write(row, 6, customer.type1_color, font_style)
            ws.write(row, 7, customer.type2_quant, font_style)
            ws.write(row, 8, customer.type2_color, font_style)
            ws.write(row, 9, customer.type2_string, font_style)
            ws.write(row, 10, customer.message, font_style)
                
        row += 1
        ws.write(row, 3, "TOTAL NEW CUSTOMERS", font_style)
        ws.write(row, 4, len(customers), font_style)
        
        wb.save(response)
            
        return response
            
    else:
        
        messages.success(request, 'Sorry, no new buyers yet!', fail_silently=False)
        return redirect('index')

def masks_dash(request):
    
    customers = ContactSender.objects.all().filter(marked=False)
    context = {
        'customers' : customers
    }
    
    return render(request, 'initiatives/masks_dash.htm', context)
    
def mark_order(request, pk):
    order = get_object_or_404(ContactSender, pk = pk)
    order.marked = True
    order.save()
    
    return redirect('masks_dash')

def tnc(request):
    return render(request, 'initiatives/tnc.htm')

def privacy_policy(request):
    return render(request, 'initiatives/ppc.htm')
    
def error_404(request, exception=None):
    return render(request, 'initiatives/404.htm', status=404)

def error_403(request, exception=None):
    return render(request, 'initiatives/403.htm', status=403)

def error_400(request, exception=None):
    return render(request, 'initiatives/400.htm', status=400)

def error_500(request, exception=None):
    return render(request, 'initiatives/503.htm', status=500)