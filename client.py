import socket

sock = socket.socket()
#   print "Enter IP address of naming server:"
#   namingServer = raw_input()
sock.connect(('localhost', 8080))

print "Text to send:",
text = raw_input()
sock.send(text)

data = sock.recv(1024)  # 1 KB
sock.close()

print data