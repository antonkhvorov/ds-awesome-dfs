FROM python:2.7-slim

WORKDIR /naming_app

ADD . /naming_app

# connection for Storage servers
EXPOSE 9000

# connection for Clients
EXPOSE 9001

ENV NAME Naming

CMD ["python", "naming_server.py"]