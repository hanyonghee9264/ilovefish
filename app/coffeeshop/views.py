from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from .models import Coffee, CoffeeCategory, CoffeeImage


def starbucks_total_list(request):
    starbucks = Coffee.objects.filter(coffeeshop_list='STARBUCKS')

    # pagination (전체보기 적용)
    paginator = Paginator(starbucks, 6)
    page = request.GET.get('page')

    try:
        starbucks = paginator.page(page)
    except PageNotAnInteger:
        starbucks = paginator.page(1)
    except EmptyPage:
        starbucks = paginator.page(paginator.num_pages)

    # url의 쿼리스트링을 가져옴. 없는 경우 None을 리턴
    calorie = request.GET.get('calorie', '')

    if calorie == 'high':
        starbucks = Coffee.objects.filter(coffeeshop_list='STARBUCKS').order_by('-calorie')
        return render(request, 'coffeeshop/starbucks_total_list.html', {'starbucks': starbucks})

    elif calorie == 'low':
        starbucks = Coffee.objects.filter(coffeeshop_list='STARBUCKS').order_by('calorie')
        return render(request, 'coffeeshop/starbucks_total_list.html', {'starbucks': starbucks})

    context = {
        'starbucks': starbucks,
    }
    return render(request, 'coffeeshop/starbucks_total_list.html', context)


def starbucks_category_coffee(request, category):
    coffee = Coffee.objects.filter(coffeeshop_list='STARBUCKS').filter(category__name__contains=category)
    # url의 쿼리스트링을 가져옴. 없는 경우 None을 리턴
    calorie = request.GET.get('calorie', 'None')

    if calorie == 'high':
        coffee = Coffee.objects.filter(category__name__contains=category).order_by('-calorie')
        return render(request, 'coffeeshop/starbucks_category_coffee.html', {'coffee': coffee})

    elif calorie == 'low':
        coffee = Coffee.objects.filter(category__name__contains=category).order_by('calorie')
        return render(request, 'coffeeshop/starbucks_category_coffee.html', {'coffee': coffee})

    context = {
        'coffee': coffee,
    }
    return render(request, 'coffeeshop/starbucks_category_coffee.html', context)


# 투썸 커피 전체보기
def twosome_total_list(request):
    twosome = Coffee.objects.filter(coffeeshop_list='ATWOSOMEPLACE')

    # pagination (전체보기 적용)
    paginator = Paginator(twosome, 6)
    page = request.GET.get('page')

    try:
        twosome = paginator.page(page)
    except PageNotAnInteger:
        twosome = paginator.page(1)
    except EmptyPage:
        twosome = paginator.page(paginator.num_pages)

    # url의 쿼리스트링을 가져옴. 없는 경우 None을 리턴
    calorie = request.GET.get('calorie', '')

    if calorie == 'high':
        twosome = Coffee.objects.filter(coffeeshop_list='ATWOSOMEPLACE').order_by('-calorie')
        return render(request, 'coffeeshop/twosome_total_list.html', {'twosome': twosome})

    elif calorie == 'low':
        twosome = Coffee.objects.filter(coffeeshop_list='ATWOSOMEPLACE').order_by('calorie')
        return render(request, 'coffeeshop/twosome_total_list.html', {'twosome': twosome})

    context = {
        'twosome': twosome,
    }
    return render(request, 'coffeeshop/twosome_total_list.html', context)


# 투썸 커피 카테고리
def twosome_category_coffee(request, category):
    coffee = Coffee.objects.filter(coffeeshop_list='ATWOSOMEPLACE').filter(category__name__contains=category)

    calorie = request.GET.get('calorie', 'None')

    if calorie == 'high':
        coffee = Coffee.objects.filter(category__name__contains=category).order_by('-calorie')
        return render(request, 'coffeeshop/twosome_category_coffee.html', {'coffee': coffee})

    elif calorie == 'low':
        coffee = Coffee.objects.filter(category__name__contains=category).order_by('calorie')
        return render(request, 'coffeeshop/twosome_category_coffee.html', {'coffee': coffee})

    context = {
        'coffee': coffee,
    }
    return render(request, 'coffeeshop/twosome_category_coffee.html', context)
