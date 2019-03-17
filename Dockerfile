FROM python:3.7.2-alpine
EXPOSE 6003

COPY requirements /requirements

RUN pip install -r /requirements/server.txt

COPY net_cloud /net_cloud

CMD [ "sh", "/net_cloud/server/entrypoint.sh" ]
