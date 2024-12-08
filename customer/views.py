from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Customer
from django.contrib import messages

# Create your views here.
def addcustomer(request):
    if request.method == 'POST':
        try:
            print("views get called")
            # Get data from POST request
            first_name = request.POST.get('firstName')
            last_name = request.POST.get('lastName')
            email = request.POST.get('customerEmail')
            phone = request.POST.get('customerPhone')
            gst_number = request.POST.get('customerGST')
            address = request.POST.get('customerAddress')
            state = request.POST.get('customerState')
            city = request.POST.get('customerCity')
            landmark = request.POST.get('customerLandmark')
            print(first_name, last_name, email, phone, gst_number, address, state, city, landmark)

            # Create new customer instance
            customer = Customer(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                gst_number=gst_number,
                address=address,
                state=state,
                city=city,
                landmark=landmark
            )
            
            # Save the customer
            customer.save()
            
            # If it's an AJAX request, return JSON response
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Customer added successfully',
                    'customer_id': customer.id
                })
            
            # For regular form submission
            messages.success(request, 'Customer added successfully!')
            return redirect('viewcustomer')

        except Exception as e:
            # Handle any errors
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                }, status=400)
            
            messages.error(request, f'Error adding customer: {str(e)}')
            return render(request, 'customer/addcustomer.html')

    # For GET request, just render the form
    return render(request, 'customer/addcustomer.html')

def viewcustomer(request):
    customers = Customer.get_all_customers()
    return render(request, 'customer/viewcustomer.html', {'customers': customers})