import datetime

from django.core.mail import EmailMessage

from coffeeshop.crawling.starbucks import Starbucks
from config import celery_app


@celery_app.task(name='starbucks_crawling')
def starbucks_crawling():
    Starbucks.get_coffee_info()

    # 위의 크롤링 함수가 종료되면 내 이메일 계정에 보고
    now_date = datetime.datetime.now().strftime('%Y-%m-%d')

    crawling_result = f'{now_date} 에 대한 크롤링 완료 메세지'
    to_email = 'hanyonghee9264@gmail.com'

    email = EmailMessage(crawling_result, )
    # EmailMessage
    print('종료')
