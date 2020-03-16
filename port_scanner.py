import optparse
#from socket import *
from threading import *
from termcolor import colored
import socket

screenLock = Semaphore(value=1)

def conn_scan(tgt_host, tgt_port):

	try:
		connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		connection.connect((tgt_host, tgt_port))
		connection.send('GET / HTTP/1.1\r\nHost: localhost\r\n\r\n'.encode())
		results = connection.recv(4096)
		
		print(results.decode())
		
		screenLock.acquire()
		print(colored('[+] {} TCP open'.format(tgt_port), 'green'))
#		print(colored('[+] '+ results.decode(), 'green'))
	
	except:
		screenLock.acquire()
		print(colored('[-] {} TCP closed\n'.format(tgt_port), 'red'))
		
	finally:
		screenLock.release()
		#connection.close()


def port_scan(tgt_host, tgt_ports):

	try:
		tgt_IP = gethostbyname(tgt_host)
	except:
		print('Cannot resolve {}: Unknown Host'.format(tgt_host))
		return
	
	try:
		tgt_name = gethostbyaddr(tgt_IP)
		print('Scan results for '+ tgt_name[0])
	except:
		print('Scan results for '+ tgt_IP)
	
	setdefaulttimeout(1)
	
	for tgt_port in tgt_ports:
		t = Thread(target=conn_scan, args=(tgt_host, int(tgt_port)))
		t.start()

def main():

	parser = optparse.OptionParser('Usage%Prog -H <target host> -p <target ports>')
	parser.add_option('-H', dest='tgtHost', type='string', help='Target Host Address')
	parser.add_option('-p', dest='tgtPort', type='string', help='Target Port numbers')

	(options, args) = parser.parse_args()

	tgt_host = options.tgtHost
	tgt_ports = str(options.tgtPort).split(',')

	if tgt_host == None or tgt_ports == None:
		print(parser.usage)
		exit(0)
		
	port_scan(tgt_host, tgt_ports)


if __name__ == '__main__':
	main()


