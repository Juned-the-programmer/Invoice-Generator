from django.shortcuts import render
from customer.models import Customer
from product.models import Product
# Create your views here.
def estimate_invoice(request):
    context = {
        'customers': Customer.objects.all(),
        'products': Product.objects.all(),
    }
    return render(request, 'estimate/estimate.html', context)