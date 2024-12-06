from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product

# Create your views here.
def addproduct(request):
    if request.method == 'POST':
        try:
            # Get data from POST request
            hsn_code = request.POST.get('hsn_code')
            name = request.POST.get('productName')
            category = request.POST.get('category')
            unit = request.POST.get('unit')
            price = request.POST.get('price')
            description = request.POST.get('description')

            # Create new product instance
            product = Product(
                hsn_code=hsn_code,
                name=name,
                category=category,
                unit=unit,
                price=price,
                description=description
            )
            
            # Save the product
            product.save()
            
            # Add success message
            messages.success(request, 'Product added successfully!')
            
            # Redirect to view products page
            return redirect('viewproduct')
            
        except Exception as e:
            # Handle any errors
            messages.error(request, f'Error adding product: {str(e)}')
            
    # For GET request, render form with choices
    context = {
        'category_choices': Product.CATEGORY_CHOICES,
        'unit_choices': Product.UNIT_CHOICES
    }
    return render(request, 'product/addproduct.html', context)

def viewproduct(request):
    products = Product.objects.all()
    return render(request, 'product/viewproduct.html', {'products': products})
