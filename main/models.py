from django.db import models


class ContactSender(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=12)
    address = models.TextField(max_length=255)
    message = models.TextField(max_length=500)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


# Create your models here.
