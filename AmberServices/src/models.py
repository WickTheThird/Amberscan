from django.db import models
from django.db import models
import uuid


class Clients(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(default=f"Client {str(id)}", max_length=50)
    email = models.EmailField(max_length=50, blank=True)
    password = models.CharField(max_length=50, blank=False)

class Providers(models.Model):
    client = models.ForeignKey('Clients', on_delete=models.CASCADE)
    signature = models.CharField(max_length=256, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    key_identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Provider: {self.client} - Active: {self.is_active}"



class Images(models.Model):

    provider = models.CharField(("Receipt Provider"), max_length=50)
    client = models.CharField(("Receipt Client"), max_length=50)
    name = models.CharField(("ReceiptName"), max_length=50)
    image = models.ImageField(upload_to=f'images/{client.name}/Receipts/')


class PDFs(models.Model):

    provider = models.CharField(("Receipt Provider"), max_length=50)
    client = models.CharField(("Receipt Client"), max_length=50)
    name = models.CharField(("ReceiptName"), max_length=50)
    pdf = models.FileField(upload_to=f'pdf/{client.name}/Receipts/')
