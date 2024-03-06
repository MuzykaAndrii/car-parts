FROM python:3.11-alpine

EXPOSE 8000
WORKDIR /site

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /site
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /site

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --noinput

ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]