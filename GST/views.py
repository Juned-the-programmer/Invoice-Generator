from django.shortcuts import render
from django.http import HttpResponse
from customer.models import Customer
from product.models import Product
from django.template.loader import render_to_string
from weasyprint import HTML
import json
from num2words import num2words
from django.conf import settings
import os

# Create your views here.

# Path to the bill number JSON file
BILL_NUMBER_FILE = os.path.join(settings.BASE_DIR, "GST/bill_number.json")

def get_current_bill_number():
    """Get the current bill number from the JSON file."""
    if not os.path.exists(BILL_NUMBER_FILE):
        with open(BILL_NUMBER_FILE, "w") as file:
            json.dump({"current_bill_no": "001"}, file)
    with open(BILL_NUMBER_FILE, "r") as file:
        data = json.load(file)
        return data["current_bill_no"]

def increment_bill_number():
    """Increment the bill number in the JSON file."""
    current_bill_no = get_current_bill_number()
    new_bill_no = str(int(current_bill_no) + 1).zfill(3)
    with open(BILL_NUMBER_FILE, "w") as file:
        json.dump({"current_bill_no": new_bill_no}, file)
    return current_bill_no


def GST_Invoice(request):
    if request.method == 'GET':
        bill_no = get_current_bill_number()
        context = {
            'bill_number' : bill_no,
            'customers': Customer.get_all_customers(),
            'products': Product.get_all_products(),
        }
        return render(request, 'GST/GST.html', context)
    
    elif request.method == 'POST':
        try:
            # Parse JSON data from request
            data = json.loads(request.body)
            
            # Get customer details
            customer = Customer.objects.get(id=data.get('customerId'))

            # Get grandTotal and handle conversion
            grand_total = data.get('grandTotal', '0')  # Default to '0' if not provided
            try:
                grand_total = float(grand_total)  # Convert to float
            except ValueError:
                return HttpResponse("Invalid grandTotal value", status=400)

            #Get the Rupee in words
            integer_part = int(grand_total)
            decimal_part = round(grand_total % 1 * 100)  # Get decimal places as integer
            rupee_in_word = f"{num2words(integer_part)} rupees and {num2words(decimal_part)} paise"
            
            # Prepare context for invoice template
            context = {
                'bill_date': data.get('billDate'),
                'bill_number': data.get('billNo'),
                'customer': customer,
                'products': data.get('products', []),
                'sub_total': data.get('subTotal'),
                'total_sgst': data.get('total_sgst', '0.00'),
                'total_cgst': data.get('total_cgst', '0.00'),
                'total_igst': data.get('total_igst', '0.00'),
                'grand_total': data.get('grandTotal'),
                'rupee_in_word': rupee_in_word
            }
            
            # Render invoice template to HTML
            html_string = render_to_string('GST/invoice_template.html', context)
            
            # Generate PDF
            html = HTML(string=html_string)
            pdf = html.write_pdf()
            
            # Create response
            response = HttpResponse(pdf, content_type='application/pdf')
            increment_bill_number()

            response['Content-Disposition'] = 'inline; filename="invoice.pdf"'
            return response
            
        except Exception as e:
            return HttpResponse(str(e), status=500)