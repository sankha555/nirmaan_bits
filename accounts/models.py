from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from initiatives.models import Initiative

class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    bits_id = models.CharField(verbose_name = "BITS ID", max_length=15, unique = True)
    year = models.IntegerField(default = 1)
    phone = models.CharField(max_length=13)
    image = models.ImageField(upload_to='media/volunteer_pics', default = None)
    
    project = models.ForeignKey(Initiative, on_delete=models.CASCADE, related_name = 'project')
    is_pl = models.BooleanField(default = False)
    visits = models.IntegerField(default = 0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height>400 or img.width > 400:
            output_size = (400, 400)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Visitor(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique = True)
    phone = models.CharField(max_length=13)
     



# Create your models here.
