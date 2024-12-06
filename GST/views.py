from django.shortcuts import render

# Create your views here.
def GST_Invoice(request):
    return render(request, 'GST/GST.html')