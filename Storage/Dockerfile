FROM python:2.7-slim

WORKDIR /storage_app

ADD . /storage_app

# connection for the heartbeat
EXPOSE 9003

# Naming server ip could be passed by -e NAMING_IP=<your ip>
# This is a default value for naming ip
ENV NAMING_IP 172.17.0.2

CMD ["sh", "-c", "python storage.py ${NAMING_IP}"]