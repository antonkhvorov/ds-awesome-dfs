# Distributed File System

* Rustam Gafarov
* Anton Khvorov
* Evgenia Lyashenko
* Alexander Simonenko

# How to run

Instead of different machines you could use different consoles
#### On Naming node:

```
cd Naming
docker build -t naming .
docker run naming
```
Remember naming node ip.

#### On each storage nodes:
```
cd Storage
docker build -t storage .
docker run -e NAMING_IP=<naming node ip> storage
```

#### On client machine:
```
cd Client
python client.py <naming node ip>
```
