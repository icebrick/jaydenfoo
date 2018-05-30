FROM python:3

ENV ENV='production'

RUN mkdir /code

WORKDIR /code

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic && mkdir media

EXPOSE 80
