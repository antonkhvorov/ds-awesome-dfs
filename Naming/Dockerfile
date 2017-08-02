FROM python:2.7-slim

WORKDIR /naming_app

ADD . /naming_app

# connection from Clients
EXPOSE 9000

# connection to Naming
EXPOSE 9001

ENV NAME Naming

CMD ["python", "naming_server.py"]