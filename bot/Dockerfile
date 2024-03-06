FROM python:3.11-alpine

WORKDIR /bot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /bot
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /bot

ENTRYPOINT ["python3"]
CMD ["main.py"]