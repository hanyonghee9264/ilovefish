from django.http import HttpResponse
from django.shortcuts import render

def starbucks_list(request):
    return render(request, 'coffeeshop/starbucks_list.html')