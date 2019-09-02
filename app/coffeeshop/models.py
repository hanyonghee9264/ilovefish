from django.db import models


def coffee_path(instance, filename):
    starbucks = 'starbucks'
    twosome = 'ATwosomePlace'

    if instance.coffee.coffeeshop_list == 'STARBUCKS':
        starbucks_path = f'{starbucks}/{instance.coffee.name}.jpg'
        return starbucks_path
    elif instance.coffee.coffeeshop_list == 'ATWOSOMEPLACE':
        twosome_path = f'{twosome}/{instance.coffee.name}.jpg'
        return twosome_path


class CoffeeCategory(models.Model):
    name = models.CharField('카테고리', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = f'{verbose_name} 목록'


class Coffee(models.Model):
    COFFEESHOP_LIST = (
        ('STARBUCKS', '스타벅스'),
        ('ATWOSOMEPLACE', '투썸플레이스'),
    )
    category = models.ForeignKey(
        CoffeeCategory,
        on_delete=models.SET_NULL,
        verbose_name='카테고리',
        null=True,
    )
    coffeeshop_list = models.CharField(max_length=20, choices=COFFEESHOP_LIST)
    name = models.CharField('커피', max_length=100)
    coffee_info = models.TextField('커피소개', blank=True,)
    coffee_size = models.CharField('커피사이즈', max_length=80, blank=True,)
    calorie = models.IntegerField('칼로리', blank=True, null=True)
    calorie_large = models.IntegerField('라지사이즈칼로리', blank=True, null=True)
    saturated_fat = models.CharField('포화지방', max_length=80, blank=True,)
    protein = models.CharField('단백질', max_length=80, blank=True,)
    sodium = models.CharField('나트룸', max_length=80, blank=True,)
    sugars = models.CharField('당류', max_length=80, blank=True,)
    caffeine = models.CharField('카페인', max_length=80, blank=True,)
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
    location = models.ImageField('커피이미지', upload_to=coffee_path, blank=True)
    coffee = models.ForeignKey(
        Coffee,
        on_delete=models.CASCADE,
        verbose_name='커피'
    )
    created_at = models.DateTimeField('등록일', auto_now_add=True)

    def __str__(self):
        return '{coffee}'.format(
            coffee=self.coffee,
        )

    class Meta:
        verbose_name = '커피이미지'
        verbose_name_plural = f'{verbose_name} 목록'
