from django.db import models
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Candy', 'Candy'),
        ('Cup', 'Cup'),
        ('Cone', 'Cone'),
    ]
    
    UNIT_CHOICES = [
        ('Box', 'Box'),
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

    @classmethod
    def get_all_products(cls):
        # Try to get products from cache
        products = cache.get('all_products')
        if products is None:
            # If not in cache, get from database
            products = list(cls.objects.all())
            # Store in cache for future use
            cache.set('all_products', products, timeout=None)  # No timeout
        return products

# Signal handlers to update cache when products are changed
@receiver(post_save, sender=Product)
def update_product_cache(sender, instance, **kwargs):
    # Update the cache when a product is added or modified
    products = list(Product.objects.all())
    cache.set('all_products', products, timeout=None)

@receiver(post_delete, sender=Product)
def delete_product_cache(sender, instance, **kwargs):
    # Update the cache when a product is deleted
    products = list(Product.objects.all())
    cache.set('all_products', products, timeout=None)
