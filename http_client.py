import sys
from socket import *
#parse the input website and find host name, path and port
def serverName(argv):
	if "https://" in argv:
		print "Https Error"
		exit(1)
	if "http://" in argv:
		argv=argv[7:]
	else:
		exit(1)
	slashIndex=argv.find('/')
	portIndex=argv.find(':')
	port=80
	path='/'

	if slashIndex!=-1 and portIndex!=-1: #argv has suffix and port
		addr=argv[:portIndex]
		path=argv[slashIndex:]
		port=argv[portIndex+1:slashIndex]
	elif slashIndex!=-1:#argv has suffix and no port
		addr=argv[:slashIndex]
		path=argv[slashIndex:]
	else:
		addr=argv

	return (addr,path,int(port))

#this is the client code
def client(webaddr):

	name,path,port=serverName(webaddr)
	addr=(name,port)	
	clientmessage="GET "+path+" HTTP/1.0\r\nHost: "+name+"\r\n\r\n"
	clientSocket=socket(AF_INET, SOCK_STREAM)# handshaking
	clientSocket.connect(addr)
	clientSocket.send(clientmessage.encode())# send request
	message= clientSocket.recv(4096)# get first chunk of respense message
	if "Content-Type: text/html" in message:
		parse(message, clientSocket)
	else:
		exit(1)
	clientSocket.close()

# parse response message
def parse(message, clientSocket):
	messages = message.split("\n")
	msgs=messages[0]
	htmlIndex=message.find("\r\n\r\n")
	html=message[htmlIndex+4:]
	codeIndex=msgs.find(" ")
	code=int(msgs[codeIndex+1:codeIndex+4])
	# print html
	if code>=400:
		printHTML(html, clientSocket)
		clientSocket.close()
		exit(1)
	elif code>=300:
		for i in messages:
			if "Location" in i:
				position=i.find(":")
				webaddr=i[position+2:-1]
				if code == 301:
					print "301 permanent redirect. Redirected to: "+webaddr
				elif code == 302:
					print "302 temporary redirect. Redirected to: "+webaddr
				break
		clientSocket.close()
		client(webaddr)
	elif code>=200:
		printHTML(html, clientSocket)
		clientSocket.close()
		exit(0)	

# to handle large website, seperate response message to many chunks. 
def printHTML(html, clientSocket):
	chunk = clientSocket.recv(4096)
	while chunk:
		html += chunk
		chunk = clientSocket.recv(4096)
	print html
	
def main(argv):
	webaddr=argv[0]
	client(webaddr)

if __name__== "__main__":
	main(sys.argv[1:])
