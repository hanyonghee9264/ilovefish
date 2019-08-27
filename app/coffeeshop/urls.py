from django.urls import path

from . import views

app_name = 'coffeeshop'

urlpatterns = [
    path('starbucks/', views.starbucks_total_list, name='starbucks'),
    path('starbucks/<str:category>/', views.starbucks_category_coffee, name='starbucks-category'),
    path('twosomeplace/', views.twosome_total_list, name='twosome'),
]