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
BUSINESS_STATE = "Gujarat"

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

            products = data.get('products', [])

            # Recalculate totals on the server to avoid client-side trust issues
            try:
                sub_total = 0.0
                total_cgst = 0.0
                total_sgst = 0.0
                total_igst = 0.0

                is_intra_state = customer.state.strip().lower() == BUSINESS_STATE.lower()

                for p in products:
                    qty = float(p.get('quantity', 0) or 0)
                    rate = float(p.get('rate', 0) or 0)
                    amount = rate * qty
                    sub_total += amount

                    gst_rate = float(p.get('gst_rate', 5) or 0)
                    gst_amount = (amount * gst_rate) / 100

                    if is_intra_state:
                        cgst = gst_amount / 2
                        sgst = gst_amount / 2
                        igst = 0
                    else:
                        cgst = 0
                        sgst = 0
                        igst = gst_amount

                    total_cgst += cgst
                    total_sgst += sgst
                    total_igst += igst

                grand_total = sub_total + total_cgst + total_sgst + total_igst
            except ValueError:
                return HttpResponse("Invalid numeric value in products", status=400)

            #Get the Rupee in words
            integer_part = int(grand_total)
            decimal_part = round(grand_total % 1 * 100)  # Get decimal places as integer
            rupee_in_word = f"{num2words(integer_part)} rupees and {num2words(decimal_part)} paise"
            
            # Prepare context for invoice template
            context = {
                'bill_date': data.get('billDate'),
                'bill_number': data.get('billNo'),
                'vehicle_number' : data.get('vehicleNo'),
                'customer': customer,
                'products': products,
                'sub_total': f"{sub_total:.2f}",
                'total_sgst': f"{total_sgst:.2f}",
                'total_cgst': f"{total_cgst:.2f}",
                'total_igst': f"{total_igst:.2f}",
                'grand_total': f"{grand_total:.2f}",
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