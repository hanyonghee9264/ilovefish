from django.contrib import admin

from coffeeshop.crawling.starbucks import Starbucks
from .models import CoffeeCategory, Coffee, CoffeeImage, CronLog

admin.site.register(CoffeeCategory)
# admin.site.register(Coffee)
admin.site.register(CoffeeImage)


def starbucks_crawling(modeladmin, request, queryset):
    Starbucks.get_coffee_info()


# 스타벅스 커피 list 형식
@admin.register(Coffee)
class CoffeeAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = (
        'name', 'coffee_size', 'calorie',
        'saturated_fat', 'protein', 'sodium', 'sugars',
        'caffeine',
    )
    search_fields = ('name',)
    actions = [starbucks_crawling]


admin.site.register(CronLog)
