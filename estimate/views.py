from django.shortcuts import render
from customer.models import Customer
from product.models import Product

def estimate_invoice(request):
    context = {
        'customers': Customer.get_all_customers(),
        'products': Product.get_all_products(),
    }
    return render(request, 'estimate/estimate.html', context)