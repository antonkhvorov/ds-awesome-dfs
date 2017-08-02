FROM python:2.7-slim

WORKDIR /storage_app

ADD . /storage_app

# connections from clients
EXPOSE 9001

# connection for the heartbeat
EXPOSE 9002

ENV NAME Storage

# Naming server ip could be passed by -e NAMING_IP=<your ip>
ENV NAMING_IP 172.17.0.2

CMD ["sh", "-c", "python storage.py ${NAMING_IP}"]