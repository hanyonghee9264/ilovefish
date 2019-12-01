from django.shortcuts import render


def main_page(request):
    return render(request, 'coffeeshop/coffeecalorie_main_page.html')
