FROM python:3.7-slim-stretch

COPY . .

RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD [ "python", "index.py" ]
