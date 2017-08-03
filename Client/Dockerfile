FROM python:2.7-slim

WORKDIR /client_app

ADD . /client_app
# Naming server ip could be passed by -e NAMING_IP=<your ip>
# This is a default value for naming ip
ENV NAMING_IP 172.17.0.2

CMD ["sh", "-c", "python client.py ${NAMING_IP}"]