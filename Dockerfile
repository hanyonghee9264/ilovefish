FROM            hanyonghee9264/coffeecalorie:base
ENV             DJANGO_SETTINGS_MODULE  config.settings.production

# Image의 /srv/project/폴더 내부에 복사
COPY            ./  /srv/projects
WORKDIR         /srv/projects

# 프로세스 실행할 명령
WORKDIR         /srv/projects/app
RUN             python3 manage.py collectstatic --noinput

# Nginx
# 기존 존재하던 Nginx설정파일 삭제
RUN             rm -rf /etc/nginx/sites-available/* && \
                rm -rf /etc/nginx/sites-enabled/* && \
                cp -f  /srv/projects/.config/app.nginx \
                       /etc/nginx/sites-available/ && \
                ln -sf /etc/nginx/sites-available/app.nginx \
                       /etc/nginx/sites-enabled/app.nginx

# supervisor 설정파일 복사
RUN             cp -f  /srv/projects/.config/supervisord.conf \
                       /etc/supervisor/conf.d/

EXPOSE          80

# Command로 supervisor 실행
CMD             supervisord -n