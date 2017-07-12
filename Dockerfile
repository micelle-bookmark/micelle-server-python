
FROM registry.cn-hangzhou.aliyuncs.com/soren/python:v2.7

MAINTAINER sorenyang@foxmail.com

RUN mkdir -p /data/www

COPY ./app/ /data/www
COPY ./conf/app.ini /etc/uwsgi/apps-enabled/app.ini
COPY ./conf/app.conf /etc/supervisor/conf.d/app.conf

WORKDIR /data/www
RUN apt-get update \
    && PACKAGES="uwsgi uwsgi-plugin-python supervisor" \
    && apt-get install -y --no-install-recommendeds ${PACKAGES} \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -r requirements.txt

WORKDIR /

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/app.conf"]
