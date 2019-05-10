import os

import boto3

from config.settings import dev
from config.settings.base import CHROME_DRIVER
from ..models import CoffeeCategory, CoffeeImage, Coffee
from config.settings.base import MEDIA_ROOT
from django.core.files import File

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import urllib.request


class Starbucks:
    def __init__(self, name, info, size, calorie, fat, protein, sodium, sugar, caffeine):
        self.name = name
        self.info = info
        self.size = size
        self.calorie = calorie
        self.fat = fat
        self.protein = protein
        self.sodium = sodium
        self.sugar = sugar
        self.caffeine = caffeine

    @classmethod
    def get_coffee_info(cls):
        chrome_options = Options()
        # chrome_options.add_argument('headless')
        # chrome_options.add_argument('disable-gpu')

        chromedriver_dir = os.path.join(CHROME_DRIVER, 'chromedriver')
        driver = webdriver.Chrome(chromedriver_dir, chrome_options=chrome_options)
        driver.get('http://www.istarbucks.co.kr/menu/drink_list.do')
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        dt_category = soup.select('dl.product_view_tab > dd > div.product_list > dl > dt > a')
        dd_content = soup.select('dl.product_view_tab > dd > div.product_list > dl > dd')

        for a, b in zip(dt_category, dd_content):
            # 카테고리 타이틀
            category_title = a.get_text(strip=True)
            category, is_category = CoffeeCategory.objects.get_or_create(
                name=category_title
            )
            # 커피 이름 & 이미지 URL & 커피 디테일 URL
            coffee_name_image_list = b.select('ul > li.menuDataSet')
            for name_image in coffee_name_image_list:
                coffee_name = name_image.select_one('dl > dd').get_text()
                # if '아이스 제주 유자 그린 티' in coffee_name:
                #     continue
                # elif '애프리콧 조이풀 티' in coffee_name:
                #     continue
                # elif '제주 유자 그린 티' in coffee_name:
                #     continue
                # elif '아이스 제주 한라봉 눈꽃 라떼' in coffee_name:
                #     continue
                # elif '제주 한라봉 눈꽃 라떼' in coffee_name:
                #     continue
                # else:
                #     pass
                coffee_image_url = name_image.select_one('dl > dt > a > img')
                coffee_image = coffee_image_url.get('src')
                coffee_url_total = name_image.select_one('dl > dt > a')
                coffee_url = coffee_url_total.get('prod')
                coffee_base_url = 'http://www.istarbucks.co.kr/menu/drink_view.do?product_cd='

                # 커피 디테일 페이지 접근
                character = '-'
                driver.get(coffee_base_url + coffee_url)
                driver.implicitly_wait(7)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                pages_detail = soup.select('div.content02 > div.product_view_wrap1 > div.product_view_detail')
                pages_detail2 = soup.select('form > fieldset > div.product_view_info > div.product_info_content')
                if character in pages_detail:
                    pass
                    for detail in pages_detail:
                        # 커피 detail name
                        detail_names = detail.select_one('div.myAssignZone > h4').get_text(strip=True)
                        # 커피 detail info
                        detail_infos = detail.select_one('div.myAssignZone > p').get_text(strip=True)
                        # 커피 detail 제품영양정보 단위
                        detail_sizes = detail.select_one(
                            'form > fieldset > div.product_view_info > div.product_info_head '
                            '> div.product_select_wrap2 > div.selectTxt2'
                        ).get_text(strip=True)
                    for detail2 in pages_detail2:
                        # 커피 detail kcal
                        detail_kcal = detail2.select_one('ul > li.kcal > dl > dd').get_text(strip=True)
                        # 커피 detail sat_FAT
                        detail_fats = detail2.select_one('ul > li.sat_FAT > dl > dd').get_text(strip=True)
                        # 커피 detail protein
                        detail_proteins = detail2.select_one('ul > li.protein > dl > dd').get_text(strip=True)
                        # 커피 detail sodium
                        detail_sodiums = detail2.select_one('ul:nth-of-type(2) > li.sodium > dl > dd').get_text(strip=True)
                        # 커피 detail sugar
                        detail_sugars = detail2.select_one('ul:nth-of-type(2) > li.sugars > dl > dd').get_text(strip=True)
                        # 커피 detail caffeine
                        detail_caffeines = detail2.select_one('ul:nth-of-type(2) > li.caffeine > dl > dd').get_text(
                            strip=True)
                    coffee, is_coffee = Coffee.objects.get_or_create(
                        coffeeshop_list='STARBUCKS',
                        category=category,
                        name=detail_names,
                        coffee_info=detail_infos,
                        coffee_size=detail_sizes,
                        calorie=detail_kcal,
                        saturated_fat=detail_fats,
                        protein=detail_proteins,
                        sodium=detail_sodiums,
                        sugars=detail_sugars,
                        caffeine=detail_caffeines,
                    )
                    STARBUCKS_DIR = os.path.join(MEDIA_ROOT, '.starbucks')
                    STARBUCKS_IMAGE_DIR = os.path.join(STARBUCKS_DIR, f'{coffee_name}.jpg')
                    if not os.path.exists(STARBUCKS_DIR):
                        os.makedirs(STARBUCKS_DIR, exist_ok=True)
                    try:
                        urllib.request.urlretrieve(coffee_image, STARBUCKS_IMAGE_DIR)
                        f = open(os.path.join(STARBUCKS_DIR, f'{coffee_name}.jpg'), 'rb')
                        CoffeeImage.objects.get_or_create(
                            location=File(f),
                            coffee=coffee,
                        )
                        f.close()
                    except FileExistsError:
                        print('이미 존재하는 파일')

        driver.close()