from django.db import models
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    gst_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        help_text="15-digit GST number (e.g., 22AAAAA0000A1Z5)"
    )
    address = models.TextField(blank=True)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['-created_at']

    @classmethod
    def get_all_customers(cls):
        # Try to get customers from cache
        customers = cache.get('all_customers')
        if customers is None:
            # If not in cache, get from database
            customers = list(cls.objects.all())
            # Store in cache for future use
            cache.set('all_customers', customers, timeout=None)
        return customers

# Signal handlers to update cache when customers are changed
@receiver(post_save, sender=Customer)
def update_customer_cache(sender, instance, **kwargs):
    # Update the cache when a customer is added or modified
    customers = list(Customer.objects.all())
    cache.set('all_customers', customers, timeout=None)

@receiver(post_delete, sender=Customer)
def delete_customer_cache(sender, instance, **kwargs):
    # Update the cache when a customer is deleted
    customers = list(Customer.objects.all())
    cache.set('all_customers', customers, timeout=None)
