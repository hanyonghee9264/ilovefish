import requests

from .base import *

DEBUG = False

WSGI_APPLICATION = 'config.wsgi.production.application'

secrets = json.load(open(os.path.join(SECRETS_DIR, 'production.json')))

ALLOWED_HOSTS = secrets['ALLOWED_HOSTS']

DATABASES = secrets['DATABASES']

# Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TAST_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Seoul' #Celery beat가 스케줄러이기 때문에 시간에 대한 정의를 해야함

# django-storages
DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'
AWS_ACCESS_KEY_ID = secrets['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = secrets['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = secrets['AWS_STORAGE_BUCKET_NAME']
# S3버전 및 지역 지정
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = 'ap-northeast-2'

# s3
AWS_DEFAULT_ACL = None


# Health Check 도메인을 허용하는 코드 [ECS]
# try:
#     EC2_IP = requests.get('http://169.254.169.254/latest/meta-data/local-ipv4').text
#     ALLOWED_HOSTS.append(EC2_IP)
# except requests.exceptions.RequestException:
#     pass

# 로그폴더 생성
LOG_DIR = os.path.join(ROOT_DIR, '.log')
# 로그 폴더가 존재하지 않으면 폴더 생성
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(levelname)s] %(name)s (%(asctime)s)\n\t%(message)s'
        },
    },
    'handlers': {
        'file_error': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'formatter': 'default',
            'maxBytes': 10485760,
            'backupCount': 10,
        },
        'file_info': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'filename': os.path.join(LOG_DIR, 'info.log'),
            'formatter': 'default',
            'maxBytes': 10485760,
            'backupCount': 10,
        },
        # console에 StreamHandler는
        # 터미널창에 표시
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
        },
    },
    'loggers': {
        'django': {
            'handlers': [
                'file_error',
                'file_info',
                'console',
            ],
            'level': 'INFO',
            'propagate': True,
        }
    }
}


def is_ec2_linux():
    """
    Detect if we are running on an EC2 Linux Instance
    See http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/identify_ec2_instances.html
    """
    if os.path.isfile("/sys/hypervisor/uuid"):
        with open("/sys/hypervisor/uuid") as f:
            uuid = f.read()
            return uuid.startswith("ec2")
    return False


def get_linux_ec2_private_ip():
    """
    Get the private IP Address of the machine if running on an EC2 linux server
    """
    from urllib.request import urlopen
    if not is_ec2_linux():
        return None
    try:
        response = urlopen('http://169.254.169.254/latest/meta-data/local-ipv4')
        ec2_ip = response.read().decode('utf-8')
        if response:
            response.close()
        return ec2_ip
    except Exception as e:
        print(e)
        return None


private_ip = get_linux_ec2_private_ip()
if private_ip:
    ALLOWED_HOSTS.append(private_ip)
