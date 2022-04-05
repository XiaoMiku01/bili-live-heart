FROM python:3.7-slim-stretch

ENV COOKIE=""
ENV RUID="0"
ENV CRON="0 0 * * *"
ENV SERVER_CHAN_SENDKEY=""
ENV TZ="Asia/Shanghai"

COPY . .

RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD [ "python", "index.py", "--fromdocker" ]
