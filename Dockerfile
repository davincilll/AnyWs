FROM im.myhk.fun/dockerproxy/library/python:3.11.2
ENV TZ="Asia/Shanghai"
RUN pip install poetry
WORKDIR /app
EXPOSE 8000
COPY . .
# 生成requirements.txt
RUN poetry lock && poetry install --no-root
RUN chmod +x /app/entrypoint

ENTRYPOINT ["/app/entrypoint"]
