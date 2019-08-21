import os
import time
import urllib.request

from bs4 import BeautifulSoup
from django.core.files import File
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.settings.base import MEDIA_ROOT, CHROME_DRIVER_DIR
from ..models import CoffeeCategory, CoffeeImage, Coffee

# 크롤링 결과 담기 위한 dict

dict_log = {
    "updated_coffee": {
        "스타벅스": {"num": 0, "list": []},
    },
    "total_coffee": {
        "스타벅스": {"num": 0, "list": []},
    },
}


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
        chrome_options.add_argument('headless')
        chrome_options.add_argument('disable-gpu')
        # Chromedriver DevToolsActivePort file doesn't exist 해결
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')


        # Docker 환경에서 chromedriver linux로 변경
        # 로컬 환경에선 Mac OS
        if 'CHROMEDRIVER_VERSION' in os.environ:
            chrome_driver_linux = os.path.join(CHROME_DRIVER_DIR, 'chromedriver_76_linux')
            driver = webdriver.Chrome(chrome_driver_linux, chrome_options=chrome_options)
        else:
            CHROME_DRIVER = os.path.join(CHROME_DRIVER_DIR, 'chromedriver_76')
            driver = webdriver.Chrome(CHROME_DRIVER, chrome_options=chrome_options)
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
                coffee_image_url = name_image.select_one('dl > dt > a > img')
                coffee_image = coffee_image_url.get('src')
                coffee_url_total = name_image.select_one('dl > dt > a')
                coffee_url = coffee_url_total.get('prod')
                coffee_base_url = 'http://www.istarbucks.co.kr/menu/drink_view.do?product_cd='

                # 커피 디테일 페이지 접근
                driver.get(coffee_base_url + coffee_url)
                driver.implicitly_wait(15)
                # selenium 팝업창 해결
                try:
                    WebDriverWait(driver, 2.5).until(EC.alert_is_present(),
                                                     'Timed out waiting for PA creation ' +
                                                     'confirmation popup to appear.')

                    alert = driver.switch_to.alert
                    alert.accept()
                    print("alert accepted")
                except TimeoutException:
                    print("no alert")
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                pages_detail = soup.select('div.content02 > div.product_view_wrap1 > div.product_view_detail')
                pages_detail2 = soup.select('form > fieldset > div.product_view_info > div.product_info_content')
                character = soup.find_all('dd', text='-')
                if character:
                    pass
                else:
                    for detail_1, detail_2 in zip(pages_detail, pages_detail2):
                        detail_names = detail_1.select_one('div.myAssignZone > h4').get_text(strip=True)
                        # 전역변수로 dict_log 사용, 커피명 dict_log[total_coffee]에 추가
                        global dict_log
                        dict_log["total_coffee"]["스타벅스"]["num"] += 1
                        dict_log["total_coffee"]["스타벅스"]["list"].append(detail_names)
                        # 커피 detail info
                        detail_infos = detail_1.select_one('div.myAssignZone > p').get_text(strip=True)
                        # 커피 detail 제품영양정보 단위
                        detail_sizes = detail_1.select_one(
                            'form > fieldset > div.product_view_info > div.product_info_head '
                            '> div.product_select_wrap2 > div.selectTxt2'
                        ).get_text(strip=True)
                        detail_kcal = detail_2.select_one('ul > li.kcal > dl > dd').get_text(strip=True)
                        # 커피 detail sat_FAT
                        detail_fats = detail_2.select_one('ul > li.sat_FAT > dl > dd').get_text(strip=True)
                        # 커피 detail protein
                        detail_proteins = detail_2.select_one('ul > li.protein > dl > dd').get_text(strip=True)
                        # 커피 detail sodium
                        detail_sodiums = detail_2.select_one('ul:nth-of-type(2) > li.sodium > dl > dd').get_text(
                            strip=True)
                        # 커피 detail sugar
                        detail_sugars = detail_2.select_one('ul:nth-of-type(2) > li.sugars > dl > dd').get_text(
                            strip=True)
                        # 커피 detail caffeine
                        detail_caffeines = detail_2.select_one('ul:nth-of-type(2) > li.caffeine > dl > dd').get_text(
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
                        if is_coffee:
                            try:
                                urllib.request.urlretrieve(coffee_image, STARBUCKS_IMAGE_DIR)
                                f = open(os.path.join(STARBUCKS_DIR, f'{coffee_name}.jpg'), 'rb')
                                CoffeeImage.objects.get_or_create(
                                    location=File(f),
                                    coffee=coffee,
                                )
                                f.close()
                                dict_log["updated_coffee"]["스타벅스"]["list"].append(coffee_name)
                                dict_log["updated_coffee"]["스타벅스"]["num"] += 1
                            except FileExistsError:
                                print('이미 존재하는 파일')
                        time.sleep(0.8)
        driver.close()

        return dict_log
