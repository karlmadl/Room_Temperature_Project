from django.urls import path

from . import views

urlpatterns = [
    path('data/', views.index)  # our-domain.com/data/ -> this path becomes active /// do not execute index, just point to it for django to execute
]