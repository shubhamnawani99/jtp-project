# syntax=docker/dockerfile:1
FROM python:3.8-buster
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install --no-cache -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]