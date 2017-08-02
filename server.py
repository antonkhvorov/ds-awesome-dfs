import socket

sock = socket.socket()
sock.bind(('', 8080))           # listen to 8080 port
sock.listen(1)
conn, addr = sock.accept()

print 'Host connected:', addr

while True:
    data = conn.recv(1024)      # 1 KB
    if not data:
        break

    # TODO: Perform operation

    conn.send("Done!")

conn.close()
