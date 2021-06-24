from django.shortcuts import render

# Create your views here.

def index(request):
    data = [
        {'reading': 72, 'location': 'inside', 'slug': 'most-recent-inside-temp'},
        {'reading': 81, 'location': 'outside', 'slug': 'most-recent-outside-temp'},
    ]
    return render(request, 'data/index.html', {
        'temperatures': data
    })

