from coffeeshop.crawling.starbucks import Starbucks
from config import celery_app


@celery_app.task(name='starbucks_crawling')
def starbucks_crawling():
    Starbucks.get_coffee_info()
    print('종료')
