import socket
import threading
import signal
import sys

name = input('Please choose a name: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

# Thread that writes new messages
def write():
	while True:
		try:
			message = input()
			client.send(message.encode('ascii'))
		except Exception as e:
			print(e)
			sys.exit()

# Thread that receives incoming messages
def receive():
	while True:
		try:
			message = client.recv(1024).decode('ascii')

			if message == 'GETNICKNAME':
				client.send(name.encode('ascii'))
			else:
				print(message)
		except:
			print('An error occurred')
			client.close()
			break

# Handle the user pressing CTRL+C to exit
def signal_handler(sig, frame):
	print('You pressed Ctrl+C! Goodbye.\n')
	sys.exit()

signal.signal(signal.SIGINT, signal_handler)


# Start the thread that listens for messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Start the thread that writes new messages
write_thread = threading.Thread(target=write)
write_thread.start()