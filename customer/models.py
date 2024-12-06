from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    gst_number = models.CharField(
        max_length=15, 
        unique=True, 
        blank=True, 
        null=True,
        help_text="15-digit GST number (e.g., 22AAAAA0000A1Z5)"
    )
    address = models.TextField(blank=True)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['-created_at']
