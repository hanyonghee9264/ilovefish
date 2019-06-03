from django.contrib import admin

from .models import CoffeeCategory, Coffee, CoffeeImage

admin.site.register(CoffeeCategory)
# admin.site.register(Coffee)
# admin.site.register(CoffeeImage)


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


@admin.register(CoffeeImage)
class CoffeeImageAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = (
        'coffee', 'location'
    )
    search_fields = ('coffee__name',)
