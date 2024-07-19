FROM python:3.12
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

CMD python manage.py runserver 0.0.0.0:8000