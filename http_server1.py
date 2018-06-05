from socket import *
import sys
# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)
class typeerror(TypeError):
    def __init__(self, arg):
        self.args = arg

def server(port):

	#Prepare a sever socket
	serverPort=port
	serverSocket=socket(AF_INET,SOCK_STREAM)
	serverSocket.bind(('',serverPort))
	serverSocket.listen(1)

	while True:
		#Establish the connection

	    print 'Ready to serve...'

		# a.Set up a new connection from the client
	    connectionSocket, addr = serverSocket.accept()

	    try:
	    	#Read the HTTP request from the connection socket and parse it

	        message =connectionSocket.recv(1024)#Receive data from the socket.

	        filename = message.split()[1]
	        dotIndex=filename.find('.')
	        fileType=filename[dotIndex+1:]
	        if fileType != "html" and fileType != "htm":
	        	raise typeerror("TypeError")


	        f = open(filename[1:])
	        # print f

	        outputdata = f.read()

			#Send one HTTP header line into socket
	        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n")
			# Send the content of the requested file to the connection socket
	        connectionSocket.send(outputdata)

	        connectionSocket.close()

	    except IOError:
			# Send HTTP response message for file not found
	        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n")
	        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")

			# Close the client connection socket
	        connectionSocket.close()
	    except typeerror,e:
	    	connectionSocket.send("HTTP/1.1 403 Forbidden\r\n\r\n")
	        connectionSocket.send("<html><head></head><body><h1>403 Forbidden</h1></body></html>\r\n")
			connectionSocket.close()
	serverSocket.close()

def main(argv):
	port=int(argv[0])
	server(port)

if __name__== "__main__":
	main(sys.argv[1:])

