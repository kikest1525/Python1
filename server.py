import threading
import socket
import signal
import sys

host = '127.0.0.1'  # localhost
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
names = []


# Broadcast a message to every user
def broadcast(name, message):
	byteMessage = message
	if name != '':
		byteMessage = (name + ': ').encode('ascii') + byteMessage
	print(byteMessage.decode('ascii'))

	for client in clients:
		client.send(byteMessage)

# Each user gets an individual thread
def listenToUser(client):
	index = clients.index(client)
	name = names[index]
	while True:
		try:
			message = client.recv(1024)
			broadcast(name, message)
		except:
			index = clients.index(client)
			clients.remove(client)
			client.close()
			name = names[index]
			broadcast('', f'{name} left the chat'.encode('ascii'))
			names.remove(name)
			broadcast('', f'Users online: [{", ".join(names)}]'.encode('ascii'))
			break

# Listen for incoming connection requests
def receive():
	while True:
		client, address = server.accept()
		print(f'Connected with {str(address)}')
		client.send('GETNICKNAME'.encode('ascii'))
		name = client.recv(1024).decode('ascii')
		names.append(name)
		clients.append(client)

		broadcast('', f'User joined the chat: {name}\n'.encode('ascii'))
		client.send('Connected to the server!'.encode('ascii'))

		# Upon successfully connecting, set a thread that listens to that user
		thread = threading.Thread(target=listenToUser, args=(client,))
		thread.start()

print('Server is listening...')
receive()
