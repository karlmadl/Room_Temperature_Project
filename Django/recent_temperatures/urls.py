from django.urls import path
from . import views

urlpatterns = [
    path('recent-temperatures/', views.index)    # our-domain.com/recent-temperatures
]