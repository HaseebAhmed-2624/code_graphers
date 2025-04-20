FROM python:3.11

WORKDIR /usr/src/app


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
COPY .. .

#COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y netcat-openbsd

## copy entrypoint.sh
RUN sed -i 's/\r$//g' ./devops/prod/entrypoint.sh
RUN chmod +x ./devops/prod/entrypoint.sh
#
## run entrypoint.sh
ENTRYPOINT ["/usr/src/app/devops/prod/entrypoint.sh"]