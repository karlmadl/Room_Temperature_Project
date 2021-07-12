from django.shortcuts import render
from .models import TemperatureData

# Create your views here.

def index(request):
    data = TemperatureData.objects.all()
    return render(request, 'recent_temperatures/index.html', {'data': data})
