FROM ljnelson/docker-calibre-alpine
MAINTAINER houmin <houmin.wei@pku.edu.cn>

RUN apk add --no-cache python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi 

ADD crontab.txt /crontab.txt
ADD main.py /main.py
COPY entry.sh /entry.sh
RUN chmod 755 /entry.sh
RUN /usr/bin/crontab /crontab.txt

VOLUME ["/data"] 

CMD ["/entry.sh"]
