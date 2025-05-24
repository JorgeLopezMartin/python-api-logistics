FROM python:3.10

EXPOSE 8000

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY docker-entrypoint.sh /code/docker-entrypoint.sh

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

WORKDIR /code

ENTRYPOINT [ "bash", "docker-entrypoint.sh" ]