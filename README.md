# Distributed File System

* Rustam Gafarov
* Anton Khvorov
* Evgenia Lyashenko
* Alexander Simonenko

# How to run

Instead of different machines you could use different consoles
#### In Naming node:

```
cd Naming
docker build -t naming .
docker run -p 9000:9000 naming
```
Remember naming node ip.

#### In each storage nodes:
```
cd Storage
docker build -t storage .
docker run -e NAMING_IP=<naming node ip> storage
```