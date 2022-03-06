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
from fpdf import FPDF
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
import xlrd

ssl = (
    """
    FBBBFC95D8234969735B7467CE5834F040D769B1D6289031330C44EDEEC66330
    comodoca.com
    564083a67bf61d1
    """
)

def read_file(request):
    f = open(settings.MEDIA_ROOT + '/97547760E84535736DCCAF0137940C67.txt', 'r')
    file_content = f.read()
    #file_content = ssl
    return HttpResponse(file_content, content_type="text/plain")

def to_paise(amount):
    return float(amount*100)

def index(request):
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

def sorad(request):
    if request.method == "POST":
        form = VisitorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('about')
    else:
        form = VisitorRegistrationForm()

    return render(request, 'initiatives/sorad.html', {'form':form})

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

@login_required
def donation_bill(request):
    
    if not request.user.username =='ut':
        return redirect('index')
    
    if request.method=="POST":
        
        data = dict(request.POST)
        bill_no = str(data["bill_no"]).replace('[', '').replace(']', '').replace("'", "")
        donor_name = str(data["donor_name"]).replace('[', '').replace(']', '').replace("'", "")
        psrn_id = str(data["psrn_id"]).replace('[', '').replace(']', '').replace("'", "")
        amount = str(data["amount"]).replace('[', '').replace(']', '').replace("'", "")
        amount_iw = str(data["amount_iw"]).replace('[', '').replace(']', '').replace("'", "")
        date_donated = str(data["date_donated"]).replace('[', '').replace(']', '').replace("'", "")
        #date_gen = str(date.today())
        pdf = FPDF()
        pdf.add_page()        
        pdf.set_font("Arial", size = 15)
        pdf.rect(5, 5, 200, 287, 'D')

        pdf.image('media/nirmaan.png', 60, 10, w = 100, h = 53)

        pdf.cell(200, 10, txt = " ", 
                ln = 1, align = 'C') 
        pdf.cell(200, 10, txt = " ", 
                ln = 1, align = 'C') 
        pdf.cell(200, 10, txt = " ", 
                ln = 1, align = 'C') 
        pdf.cell(200, 10, txt = " ", 
                ln = 1, align = 'C')
        pdf.cell(200, 10, txt = " ", 
                ln = 1, align = 'C')
         

        pdf.cell(200, 10, txt = "Nirmaan Organization, BITS Pilani", 
                ln = 1, align = 'C')        
        pdf.cell(200, 10, txt = "Donation Receipt",
                ln = 2, align = 'C')
        pdf.cell(200, 10, txt = "     ",
                ln = 3, align = 'C')
        top = pdf.y
        offset = pdf.x + 90
        pdf.multi_cell(90, 10, "Bill Number: ", 1, 0)
        pdf.y = top
        pdf.x = offset 
        pdf.multi_cell(90, 10, bill_no, 1, 0)
        top = pdf.y
        offset = pdf.x + 90
        pdf.multi_cell(90, 10, "Name: ", 1, 0)
        pdf.y = top
        pdf.x = offset 
        pdf.multi_cell(90, 10, donor_name, 1, 0)
        top = pdf.y
        offset = pdf.x + 90
        pdf.multi_cell(90, 10, "PSRN ID: ", 1, 0)
        pdf.y = top
        pdf.x = offset 
        pdf.multi_cell(90, 10, psrn_id, 1, 0)
        top = pdf.y
        offset = pdf.x + 90
        pdf.multi_cell(90, 10, "Amount: ", 1, 0)
        pdf.y = top
        pdf.x = offset 
        pdf.multi_cell(90, 10, 'Rs. '+amount, 1, 0)
        top = pdf.y
        offset = pdf.x + 90
        pdf.multi_cell(90, 10, "Amount (in words): ", 1, 0)
        pdf.y = top
        pdf.x = offset 
        pdf.multi_cell(90, 10, 'Rupees '+amount_iw+'only', 1, 0)
        top = pdf.y
        offset = pdf.x + 90
        pdf.multi_cell(90, 10, "Date Donated: ", 1, 0)
        pdf.y = top
        pdf.x = offset 
        pdf.multi_cell(90, 10, date_donated, 1, 0)
        pdf.output('./media/'+bill_no+'.pdf', 'F')

        fs = FileSystemStorage()
        filename = bill_no+'.pdf'
        if fs.exists(filename):
            with fs.open(filename) as pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="'+bill_no+'.pdf"'
                return response
            
        return redirect('/donation_bill')
                
    return render(request, "initiatives/bill_form.html")

def update_projects(request):
    workbook = xlrd.open_workbook("./media/nirmaan_projects.xls")

    sheet = workbook.sheet_by_index(0)
    row_count = sheet.nrows

    for cur_row in range(1, row_count):
        name_cur = sheet.cell(cur_row, 0).value
        slug_cur = sheet.cell(cur_row, 1).value
        desc_cur = sheet.cell(cur_row, 2).value

        Initiative.objects.create(name = name_cur, slug = slug_cur, description = desc_cur, date_started = '2020-01-01')
    
    return render(request, 'initiatives/update_projects.html')

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
