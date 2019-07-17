## 커피칼로리체크 프로젝트

### 프로젝트 소개

기존의 프렌차이즈 커피점(스타벅스, 탐앤탐스 ...) 홈페이지에 커피에 대한 칼로리 정보를 확인하기 위해서

1. 전체 메뉴 중 해당 메뉴클릭
2. 원하는 커피메뉴 클릭
3. 해당 메뉴에 대한 칼로리 및 성분을 볼 수 있음

이러한 **번거로움**을 **최소화**시켜 커피에 대한 칼로리 및 성분표시를 보다 **편리하게 볼 수 있도록** **제작한 프로젝트**입니다.

### 프로젝트 URL

- [https://coffeecalorie.shop](https://coffeecalorie.shop){: target="_blank" }

### 프로젝트 개발환경 및 프로그램
- AWS Elastic Beanstalk
- AWS Elasticache
- AWS RDS
- AWS Route 53
- AWS Certificate Manager
- AWS s3
- Celery
- html
- css
- Django
- Docker
- JavaScript
- PostgreSQL
- Python
- Nginx
- uWSGI

### 주요내용
- 개발 환경 분리(dev/production)
- celery beat를 활용하여 스타벅스 체인점 커피를 매달 1일 12시에 크롤링 후 업데이트
	- 해당 크롤링 동작 후 Gmail 계정으로 결과 보고
- 해당 커피에 대한 칼로리 (높은순/낮은순) 옵션을 통한 정렬
- AWS EB 를 통해 배포
	- deploy.sh 로 배포
	- log.sh 로 로컬에서 실시간 로그 확인가능
- Sentry 설정으로 발생된 에러를 설정메일로 확인

### Requirements

```
awsebcli<3.16
boto3<1.10
bs4<0.0.2
celery<4.3.1
Django<2.2
django-crontab<0.7.2
django-celery-beat<1.4.1
django-celery-results<1.0.5
django-storages<1.8
lxml<4.3.2
Pillow<5.4
psycopg2-binary<2.8
pytz<2018.9
redis<3.2.2
requests<2.20.2
selenium<3.141.1
sentry-sdk<0.9.3

```

### Secrets
.secrets/base.json

```
  "SECRET_KEY": "<Django settings SECRET_KEY value>",
  "EMAIL_BACKEND": "django.core.mail.backends.smtp.EmailBackend",
  "EMAIL_USE_TLS": "True",
  "EMAIL_PORT": 587,
  "EMAIL_HOST": "smtp.gmail.com",
  "EMAIL_HOST_USER": "<EMAIL_HOST_USER>",
  "EMAIL_HOST_PASSWORD": "<EMAIL_HOST_PASSWORD>",
  "SERVER_EMAIL": "<SERVER_EMAIL>",
  "DEFAULT_FROM_MAIL": "<DEFAULT_FROM_MAIL>",
  "AWS_ELASTIC_CACHE": "<AWS_ELASTIC_CACHE 엔드포인트>"
```

---
```
"DATABASES": {
    "default": {
      "ENGINE": "django.db.backends.postgresql",
        "NAME": "<DB name>",
        "HOST": "<RDS endpoint>",
        "USER": "<DB username>",
        "PASSWORD": "<DB user password>",
        "PORT": 5432
    }
  },
  "AWS_ACCESS_KEY_ID" : "<AWS_ACCESS_KEY value>",
  "AWS_SECRET_ACCESS_KEY" : "<AWS_SECRET_ACCESS_KEY value>",
  "AWS_STORAGE_BUCKET_NAME" : "<AWS_STORAGE_BUCKET_NAME>",

  "SENTRY_DSN" : "https://<sentry_Client_Keys>"
```
