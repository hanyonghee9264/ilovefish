from django.db import models


class CoffeeCategory(models.Model):
    name = models.CharField('카테고리', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = f'{verbose_name} 목록'


class Coffee(models.Model):
    category = models.ForeignKey(
        CoffeeCategory,
        on_delete=models.SET_NULL,
        verbose_name='카테고리',
        null=True,
    )
    name = models.CharField('커피', max_length=50)
    coffee_info = models.TextField('커피소개', blank=True,)
    coffee_size = models.CharField('커피사이즈', max_length=80, blank=True)
    calorie = models.IntegerField('칼로리', blank=True)
    saturated_fat = models.IntegerField('포화지방', blank=True)
    protein = models.IntegerField('단백질', blank=True)
    sodium = models.DecimalField('나트룸', blank=True, max_digits=5, decimal_places=1)
    sugars = models.IntegerField('당류', blank=True)
    caffeine = models.IntegerField('카페인', blank=True)
    created_at = models.DateTimeField('등록일', auto_now_add=True)

    def __str__(self):
        return '{category}::{name}'.format(
            category=self.category,
            name=self.name,
        )

    class Meta:
        verbose_name = '커피'
        verbose_name_plural = f'{verbose_name} 목록'


class CoffeeImage(models.Model):
    location = models.ImageField('커피이미지', upload_to='starbucks_coffee', blank=True)
    coffee = models.ForeignKey(
        Coffee,
        on_delete=models.CASCADE,
        verbose_name='커피'
    )
    created_at = models.DateTimeField('등록일', auto_now_add=True)

    class Meta:
        verbose_name = '커피이미지'
        verbose_name_plural = f'{verbose_name} 목록'
