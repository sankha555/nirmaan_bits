from django.db import models
from django.utils import timezone

TYPE1_COLOR_CHOICES = [
    ('Baby Pink', 'Baby Pink'),
    ('Aqua Green', 'Aqua Green'),
]

TYPE2_COLOR_CHOICES = [
    ('White', 'White'),
    ('Black', 'Black'),
    ('Navy Blue', 'Navy Blue')
]

STRING_CHOICES = [
    ('Strings', 'Strings'),
    ('Elastic', 'Elastic'),
]

class ContactSender(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    phone = models.CharField(max_length=12, null=False, blank=False)
    address = models.TextField(max_length=255)
    pincode = models.CharField(max_length=8, default="")
    message = models.TextField(max_length=500)
    email = models.EmailField(max_length=254, null=False, blank=False, default="")
    marked = models.BooleanField(default=False)
    
    type1_color = models.CharField(choices=TYPE1_COLOR_CHOICES, default="Baby Pink", max_length=20)
    type1_quant = models.IntegerField(default=1)
    
    type2_color = models.CharField(choices=TYPE2_COLOR_CHOICES, default="White", max_length=20)
    type2_quant = models.IntegerField(default=0)
    type2_string = models.CharField(choices=STRING_CHOICES, max_length=50, default="Strings")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Donation(models.Model):
    donor_name = models.CharField(max_length=50, default="", blank=False)
    amount = models.IntegerField(default=100)
    date = models.DateTimeField(default=timezone.now())
    message = models.TextField(max_length=1000, default="", blank=True)
    #certificate = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 

# Create your models here.
