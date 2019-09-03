from django.urls import path

from . import views

app_name = 'coffeeshop'

urlpatterns = [
    path('starbucks/', views.starbucks_total_list, name='starbucks'),
    path('starbucks/<str:category>/', views.starbucks_category_coffee, name='starbucks-category'),
    path('twosomeplace/', views.twosome_total_list, name='twosome'),
    path('twosomeplace/<str:category>/', views.twosome_category_coffee, name='twosome-category'),
    path('search/', views.coffee_search_list, name='calorie-search')
]