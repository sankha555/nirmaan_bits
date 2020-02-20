from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from PIL import Image
                            
# Models for Initiatives and Events of Nirmaan Organization

class Initiative(models.Model):  
    name = models.CharField(verbose_name = "Name", max_length = 255, default = "")
    description = models.TextField(verbose_name = "Description", max_length = 1000, default = "")
    meta_description = models.TextField(verbose_name = "Meta_Description", max_length = 1000, default = description.description[:50]+"....")
    date_started = models.DateField(verbose_name = "Start Date", default = timezone.now())
    banner_image = models.ImageField(verbose_name = "Banner Image", default = "default.png", upload_to='banner_images/')
    likes = models.IntegerField(default = 0)

    ig_url = models.URLField(verbose_name = "Instagram Page URL", max_length = 255, default = "https://www.instagram.com/nirmaan_pilani/")
    fb_url = models.URLField(verbose_name = "Facebook Page URL", max_length = 255, default = "https://www.facebook.com/NirmaanPilaniPage/")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.meta_description = self.description[:50] + "...."
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
    message = models.TextField(max_length = 255, default = "")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)