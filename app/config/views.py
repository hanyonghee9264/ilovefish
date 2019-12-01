from django.shortcuts import render


def main_page(request):
    return render(request, 'coffeeshop/homepage_main.html')
