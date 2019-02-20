from django.contrib import admin

from .models import CoffeeCategory, Coffee, CoffeeImage

admin.site.register(CoffeeCategory)
admin.site.register(Coffee)
admin.site.register(CoffeeImage)


