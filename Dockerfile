FROM python:3.6-alpine

RUN adduser -D microblog

WORKDIR /home/microblog

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN /usr/bin/pipenv install
RUN /usr/bin/pipenv install gunicorn pymysql

COPY microblog_app microblog_app
COPY migrations migrations
COPY microblog.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP microblog.py

RUN chown -R microblog:microblog ./
USER microblog

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
