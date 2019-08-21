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
        "투썸플레이스": {"num": 0, "list": []},
    },
    "total_coffee": {
        "투썸플레이스": {"num": 0, "list": []},
    },
}


class Twosome:
    def __init__(self, name, info, size, calorie, fat, protein, sodium, sugar):
        self.name = name
        self.info = info
        self.size = size
        self.calorie = calorie
        self.fat = fat
        self.protein = protein
        self.sodium = sodium
        self.sugar = sugar

    @classmethod
    def get_coffee_info(cls):
        chrome_options = Options()
        # chrome_options.add_argument('headless')
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

        driver.get('https://www.twosome.co.kr:7009/menu/list.asp?rank=2')
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        # 카테고리명
        category_names = soup.select('div#content > ul.tab > li:nth-of-type(n+2)')

        # for category in category_names:
        #     category_name = category.get_text(strip=True)
        #     gb_category_name.append(category_name)
        #     category, is_category = CoffeeCategory.objects.get_or_create(
        #         name=category_name
        #     )

        # 카테고리 4개 주소 [에스프레소, 블렌디드, 티, 기타]
        category_pages_base_url = 'https://www.twosome.co.kr:7009/menu/list.asp?rank=2&c_prt_cate_idx='
        category_pages_url = ['76', '213', '214', '331']

        # 카테고리별 페이지 접근
        for a, b in zip(category_names, category_pages_url):
            category_name = a.get_text(strip=True)
            category, is_category = CoffeeCategory.objects.get_or_create(
                name=category_name
            )
            driver.get(category_pages_base_url + b)
            # Category Content
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')

            # 현재 반환되는 페이지
            div_content = soup.select('div#content > div.product-container > ul.product-list li')
            for content in div_content:
                coffee_detail_page_base_url = 'https://www.twosome.co.kr:7009/menu/'
                coffee_detail_page_url = content.select_one('p > a').get('href')

                # 디테일 페이지 접근
                driver.get(coffee_detail_page_base_url + coffee_detail_page_url)
                # selenium 팝업창 해결
                try:
                    WebDriverWait(driver, 0.2).until(EC.alert_is_present(),
                                                     'Timed out waiting for PA creation ' +
                                                     'confirmation popup to appear.')

                    alert = driver.switch_to.alert
                    alert.accept()
                    print("alert accepted")
                except TimeoutException:
                    print("no alert")

                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                # 커피 디테일 페이지
                detail_page_content = soup.select('div#content > div.line-box > div.product-view')

                # 커피 디테일 페이지 [성분표]
                for detail in detail_page_content:
                    # 커피 이미지
                    coffee_img_base_url = 'https://www.twosome.co.kr:7009/'
                    coffee_img = detail.select_one('div.thumb > div#imgView > img').get('src')
                    coffee_image = coffee_img_base_url + coffee_img
                    # 커피 이름
                    coffee_name = detail.select_one('div.product-des > p.tit02').get_text(strip=True)

                    global dict_log
                    dict_log["total_coffee"]["투썸플레이스"]["num"] += 1
                    dict_log["total_coffee"]["투썸플레이스"]["list"].append(coffee_name)

                    # 커피 설명
                    coffee_infos = detail.select_one('p.des').get_text(strip=True)
                    # 커피 디테일 페이지 [성분표]
                    coffee_table = detail.select_one('dl.nutrition > dd > ul')
                    # 커피 사이즈
                    coffee_size = coffee_table.select_one('li.total-g > span').get_text(strip=True)
                    # 커피 칼로리
                    coffee_calorie = coffee_table.select_one('li:nth-of-type(3) > span').get_text(strip=True)
                    # 커피 포화지방
                    coffee_fats = coffee_table.select_one('li:nth-of-type(6) > span').get_text(strip=True)
                    # 커피 단백질
                    coffee_protein = coffee_table.select_one('li:nth-of-type(5) > span').get_text(strip=True)
                    # 커피 나트륨
                    coffee_sodium = coffee_table.select_one('li:nth-of-type(7) > span').get_text(strip=True)
                    # 커피 당류
                    coffee_sugar = coffee_table.select_one('li:nth-of-type(4) > span').get_text(strip=True)

                    coffee, is_coffee = Coffee.objects.get_or_create(
                        coffeeshop_list='ATWOSOMEPLACE',
                        category=category,
                        name=coffee_name,
                        coffee_info=coffee_infos,
                        coffee_size=coffee_size,
                        calorie=coffee_calorie,
                        saturated_fat=coffee_fats,
                        protein=coffee_protein,
                        sodium=coffee_sodium,
                        sugars=coffee_sugar,
                    )

                    ATWOSOME_DIR = os.path.join(MEDIA_ROOT, '.twosome')
                    ATWOSOME_IMAGE_DIR = os.path.join(ATWOSOME_DIR, f'{coffee_name}.jpg')
                    if not os.path.exists(ATWOSOME_DIR):
                        os.makedirs(ATWOSOME_DIR, exist_ok=True)
                    if is_coffee:
                        try:
                            urllib.request.urlretrieve(coffee_image, ATWOSOME_IMAGE_DIR)
                            f = open(os.path.join(ATWOSOME_DIR, f'{coffee_name}.jpg'), 'rb')
                            CoffeeImage.objects.get_or_create(
                                location=File(f),
                                coffee=coffee,
                            )
                            f.close()
                            dict_log["updated_coffee"]["투썸플레이스"]["list"].append(coffee_name)
                            dict_log["updated_coffee"]["투썸플레이스"]["num"] += 1
                        except FileExistsError:
                            print('이미 존재하는 파일')
                    time.sleep(0.8)
        driver.close()

        return dict_log
