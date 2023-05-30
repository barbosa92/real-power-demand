# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

WORKDIR /power-demand

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
ENV SQLALCHEMY_DATABASE_URI=<your-database-uri>
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]