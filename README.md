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
docker run -p 9000:9000 -p 9001:9001 naming
```
Remember naming node ip.

#### On each storage nodes:
```
cd Storage
docker build -t storage .
docker run -e NAMING_IP=<naming node ip> -p 9002:9002 -p 9003:9003 storage
```

#### On client machine:
```
python dfs.py <naming node ip>
```