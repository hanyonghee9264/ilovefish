from django.shortcuts import render, get_object_or_404

from .models import Coffee, CoffeeCategory, CoffeeImage


def starbucks_total_list(request):
    details = Coffee.objects.all()
    context = {
        'details': details,
    }
    return render(request, 'coffeeshop/starbucks_total_list.html', context)


def starbucks_category_coffee(request, category):
    coffee = Coffee.objects.filter(category__name__contains=category)
    context = {
        'coffee': coffee,
    }
    return render(request, 'coffeeshop/starbucks_category_coffee.html', context)
