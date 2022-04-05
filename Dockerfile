FROM python:3.7-slim-stretch

ENV COOKIE=""
ENV RUID="0"
ENV CRON="0 0 * * *"
ENV SERVER_CHAN_SENDKEY=""
ENV TZ="Asia/Shanghai"

RUN apt-get update && apt-get install -y --no-install-recommends \
		curl unzip \
	&& rm -rf /var/lib/apt/lists/*
WORKDIR /app
# RUN git clone https://github.com/starrin/bili-live-heart.git
#RUN git clone https://github.com/XiaoMiku01/bili-live-heart.git
RUN curl -kOL https://github.com/XiaoMiku01/bili-live-heart/archive/refs/heads/master.zip && unzip master.zip
WORKDIR /app/bili-live-heart-master
# RUN git checkout dock-refine
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD [ "python", "index.py", "--fromdocker" ]
