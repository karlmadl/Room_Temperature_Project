from django.shortcuts import render
from .models import TemperatureData

# Create your views here.

def index(request):
    data = TemperatureData.objects.all()
    return render(request, 'recent_temperatures/index.html', {'data': data})


def recent_last(request):
    last_data = TemperatureData.objects.last()
    return render(request, "recent_temperatures/data.html", {'last_point': last_data})