from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils.timezone import now


class Providers(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    signature = models.CharField(max_length=256, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    key_identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Provider: {self.client} - Active: {self.is_active}"
    
    def deactivate_expired(self):

        if self.expires_at and self.expires_at < now():
            self.is_active = False
            self.save()


def upload_to_images(instance, filename):
    return f'images/{instance.client.username}/Receipts/{filename}'


def upload_to_pdfs(instance, filename):
    return f'pdf/{instance.client.username}/Receipts/{filename}'


class Images(models.Model):
    provider = models.ForeignKey(Providers, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to=upload_to_images)

    def __str__(self):
        return f"Image: {self.name} by {self.client}"


class PDFs(models.Model):
    provider = models.ForeignKey(Providers, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    pdf = models.FileField(upload_to=upload_to_pdfs)

    def __str__(self):
        return f"PDF: {self.name} by {self.client}"

class ProcessedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Images, null=True, blank=True, on_delete=models.CASCADE)
    pdf = models.ForeignKey(PDFs, null=True, blank=True, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    vat_number = models.CharField(max_length=50, null=True, blank=True)
    transaction_date = models.DateField(null=True, blank=True)
    transaction_time = models.TimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    items = models.JSONField(null=True, blank=True)
    fuel_type = models.CharField(max_length=50, null=True, blank=True)
    is_invoice = models.BooleanField(default=False)
    total_gross = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_vat = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_net = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ProcessedImage for {self.user.username} - {self.company_name or 'Unknown Company'}"

class SecretKey(models.Model):
    user = models.CharField(max_length=255, blank=True)
    key = models.CharField(default=uuid.uuid4, editable=False, unique=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SecretKey for {self.user.username}"
