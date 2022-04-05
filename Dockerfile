FROM python:3.7-slim-stretch

ENV COOKIE=""
ENV RUID="0"
ENV CRON="0 0 * * *"
ENV SERVER_CHAN_SENDKEY=""
ENV TZ="Asia/Shanghai"

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
	apt-get update && apt-get install -y --no-install-recommends \
		git \
	&& rm -rf /var/lib/apt/lists/*
WORKDIR /app
# RUN git clone https://github.com/starrin/bili-live-heart.git
#RUN git clone https://github.com/XiaoMiku01/bili-live-heart.git
# RUN curl -kOL https://github.com/XiaoMiku01/bili-live-heart/archive/refs/heads/master.zip && unzip master.zip
RUN git clone https://gitee.com/XiaoMiku01/bili-live-heart.git
# WORKDIR /app/bili-live-heart-master
WORKDIR /app/bili-live-hear
RUN git checkout dock-refine
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD [ "python", "index.py", "--fromdocker" ]
