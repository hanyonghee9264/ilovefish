from django.shortcuts import render

from .models import Coffee, CoffeeCategory


def starbucks_list(request):
    starbucks_details = Coffee.objects.all()
    context = {
        'details': starbucks_details,
    }
    return render(request, 'coffeeshop/starbucks/starbucks_list.html', context)


def starbucks_filtering(request):
    coffee = Coffee.objects.all()
    # coldbrew = Coffee.objects.filter(category__name__contains='콜드 브루 커피')
    context = {
        'coffee': coffee,
        'coldbrew': coldbrew,
    }
    return render(request, 'coffeeshop/starbucks/starbucks_coldbrew.html', context)
