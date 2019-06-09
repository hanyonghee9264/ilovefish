from django.shortcuts import render

from .models import CoffeeImage, Coffee


def starbucks_list(request):
    starbucks_details = Coffee.objects.all()
    context = {
        'details': starbucks_details,
    }
    return render(request, 'coffeeshop/starbucks_list.html', context)
