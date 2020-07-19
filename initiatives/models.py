from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True
                            
# Models for Project of Nirmaan Organization

class Initiative(models.Model):  
    name = models.CharField(verbose_name = "Name", max_length = 255, default = " ")
    slug = models.CharField(verbose_name = "Short Name", max_length = 255, default = " ")
    description = models.TextField(verbose_name = "Description", max_length = 1000, default = " ", blank=True)
    date_started = models.DateField(verbose_name = "Start Date")
    banner_image = models.ImageField(verbose_name = "Banner Image", default = "default.png", upload_to='banner_images/')
    likes = models.IntegerField(default = 0)

    volunteers_file = models.FileField(upload_to='media/volunteers_files', max_length=100, null=True)

    ig_url = models.URLField(verbose_name = "Instagram Page URL", max_length = 255, default = "https://www.instagram.com/nirmaan_pilani/")
    fb_url = models.URLField(verbose_name = "Facebook Page URL", max_length = 255, default = "https://www.facebook.com/NirmaanPilaniPage/")
    ketto_url = models.URLField(verbose_name = "Ketto Page URL", max_length = 255, default="https://www.ketto.org/")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.banner_image.path)

        if img.height>800 or img.width > 1000:
            output_size = (800, 1000)
            img.thumbnail(output_size)
            img.save(self.banner_image.path)

    def get_absolute_url(self):
        return reverse('init_detail', kwargs={'pk': self.pk})


class InitiativeComment(models.Model):
    initiative = models.ForeignKey(Initiative, on_delete=models.CASCADE, related_name='comments')
    published_on = models.DateField(default = timezone.now())
    message = models.CharField(verbose_name = "", max_length = 255, default = "")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
