from django.shortcuts import render
from django.http import FileResponse
from django.conf import settings
import os

# Create your views here.
def index(request):
    return render(request, 'pages/index.html')

def backup_database(request):
    db_path = os.path.join(settings.BASE_DIR, "db.sqlite3")
    return FileResponse(open(db_path, 'rb'), as_attachment=True, filename="db.sqlite3")