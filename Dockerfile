FROM im.myhk.fun/dockerproxy/library/python:3.11.2
ENV TZ="Asia/Shanghai"
RUN pip install poetry
# 安装相关的图像库
RUN apt-get update && apt-get -y install libz-dev libjpeg-dev libfreetype6-dev python-dev
WORKDIR /app
EXPOSE 8000
COPY . .
# 生成requirements.txt
RUN poetry lock && poetry install --no-root
RUN chmod +x /app/entrypoint

ENTRYPOINT ["/app/entrypoint"]
