FROM im.myhk.fun/dockerproxy/library/python:3.11.2
ENV TZ="Asia/Shanghai"
RUN pip install poetry
# 安装相关的图像库以及nginx
RUN apt-get update && apt-get -y install libz-dev libjpeg-dev libfreetype6-dev python-dev nginx
WORKDIR /app
EXPOSE 80
COPY app/nginx/nginx.conf /etc/nginx/nginx.conf
COPY . .
RUN poetry lock && poetry install --no-root
RUN chmod +x /app/entrypoint

# 使用一个脚本来启动Nginx和应用程序
CMD /app/entrypoint
