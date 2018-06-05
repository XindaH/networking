from socket import *
import sys
import select


class typeerror(TypeError):
    def __init__(self, arg):
        self.args = arg


def server(port):
    # Prepare a sever socket
    serverPort = port
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setblocking(0)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(5)

    # Sockets from which we expect to read
    inputs = [serverSocket]
    outputs = []
    #begin refernece from https://pymotw.com/2/select/
    while inputs:
        # Wait for at least one of the sockets to be ready for processing
        print '\nwaiting for the next event'
        readable, writable, exceptional = select.select(inputs, outputs, inputs)

        # Handle inputs
        for s in readable:
            if s is serverSocket:
                # A "readable" server socket is ready to accept a connection
                connection, client_address = s.accept()
                print 'new connection from' + bytes(client_address)
                connection.setblocking(1)
                inputs.append(connection)
        # end reference
            else:
                message = s.recv(1024)  # Receive data from the socket.
                if message:
                    try:
                        # Read the HTTP request from the connection socket and parse it
                        filename = message.split()[1]
                        dotIndex = filename.find('.')
                        fileType = filename[dotIndex + 1:]
                        if fileType != "html" and fileType != "htm":
                            raise typeerror("TypeError")

                        f = open(filename[1:])
                        # print f

                        outputdata = f.read()

                        # Send one HTTP header line into socket
                        s.send("HTTP/1.1 200 OK\r\n\r\n")
                        # Send the content of the requested file to the connection socket
                        s.send(outputdata)
                        s.send("\r\n")
                        inputs.remove(s)
                        s.close()

                    except IOError:
                        # Send HTTP response message for file not found
                        s.send("HTTP/1.1 404 Not Found\r\n\r\n")
                        s.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")

                        # Close the client connection socket
                        inputs.remove(s)
                        s.close()
                    except typeerror, e:
                        s.send("HTTP/1.1 403 Forbidden\r\n\r\n")
                        s.send("<html><head></head><body><h1>403 Forbidden</h1></body></html>\r\n")
                        inputs.remove(s)
                        s.close()
                else:
                    inputs.remove(s)
                    s.close()


def main(argv):
    port = int(argv[0])
    server(port)


if __name__ == "__main__":
    main(sys.argv[1:])
