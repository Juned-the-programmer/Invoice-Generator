from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('food', 'Food'),
        ('other', 'Other'),
    ]
    
    UNIT_CHOICES = [
        ('piece', 'Piece'),
        ('kg', 'Kilogram'),
        ('liter', 'Liter'),
        ('meter', 'Meter'),
        ('dozen', 'Dozen'),
    ]
    
    hsn_code = models.CharField(
        max_length=8,
        help_text="Enter 4-8 digit HSN code as per GST guidelines"
    )
    name = models.CharField(max_length=200)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other'
    )
    unit = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES,
        default='piece'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price in INR (₹)"
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
