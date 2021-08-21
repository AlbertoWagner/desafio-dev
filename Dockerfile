

FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

ENTRYPOINT ["./docker/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "127.0.0.1:4000"]