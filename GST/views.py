from django.shortcuts import render
from customer.models import Customer
from product.models import Product

# Create your views here.
def GST_Invoice(request):
    context = {
        'customers': Customer.objects.all(),
        'products': Product.objects.all(),
    }
    return render(request, 'GST/GST.html', context)