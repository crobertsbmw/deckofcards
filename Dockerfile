FROM python:3.6.3-alpine3.6

 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 RUN pip install -r requirements.txt
 ADD . /code/
 RUN python manage.py migrate

CMD ["python", "manage.py","runserver", "0.0.0.0:8000"]