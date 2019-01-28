FROM            ubuntu:18.04
MAINTAINER      hanyonghee9264@gmail.com

# 패키지 업그레이드, Python3설치
RUN             apt -y update
RUN             apt -y dist-upgrade
RUN             apt -y install python3-pip

# Nginx, uWSGI 설치 (Webserver, WSGI)
RUN             apt -y install nginx
RUN             pip3 install uwsgi

# Image의 /srv/project/폴더 내부에 복사
COPY            ./  /srv/project
WORKDIR         /srv/project
RUN             pip3 install -r requirements.txt

# 프로세스 실행할 명령
WORKDIR         /srv/project/app
CMD             python3 manage.py runserver 0:8000