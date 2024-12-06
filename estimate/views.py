from django.shortcuts import render

# Create your views here.
def estimate_invoice(request):
    return render(request, 'estimate/estimate.html')