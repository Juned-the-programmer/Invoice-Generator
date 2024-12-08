from django.shortcuts import render
from django.http import HttpResponse
from customer.models import Customer
from product.models import Product
from django.template.loader import render_to_string
from weasyprint import HTML
import json

# Create your views here.
def GST_Invoice(request):
    if request.method == 'GET':
        context = {
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
            
            # Prepare context for invoice template
            context = {
                'bill_date': data.get('billDate'),
                'bill_number': data.get('billNo'),
                'customer': customer,
                'products': data.get('products', []),
                'sub_total': data.get('subTotal'),
                'sgst_rate': '9',  # Adjust based on your requirements
                'cgst_rate': '9',  # Adjust based on your requirements
                'igst_rate': '18', # Adjust based on your requirements
                'total_sgst': data.get('totalSGST', '0.00'),
                'total_cgst': data.get('totalCGST', '0.00'),
                'total_igst': data.get('totalIGST', '0.00'),
                'grand_total': data.get('grandTotal')
            }
            
            # Render invoice template to HTML
            html_string = render_to_string('GST/invoice_template.html', context)
            
            # Generate PDF
            html = HTML(string=html_string)
            pdf = html.write_pdf()
            
            # Create response
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="invoice.pdf"'
            return response
            
        except Exception as e:
            return HttpResponse(str(e), status=500)