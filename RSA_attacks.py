import random
import time
from termcolor import colored

def find_p_q(e, n):
	''' This function is used to find the values of p and q. Also a condition is
		checked that the multiplication of p and q should not be equal to 0. If 
		it is zero, find other values. '''
	key_value = {}
	while True:
		p, q = random.randint(1, n), random.randint(1, n)	
		if p * q == n:
			if p == 1 or q == 1:
				continue
			break
	print('Value of p and q = ', p, q)
	return p, q

	
def brute_force(e, c, n):
	''' This function is used to find the value of message by brute forcing the	
		values of m. '''
#	m = 1
	while True:
		m = random.randint(1, 1000)
		if (m ** e) % n == c % n:
#		if (m ** e) % n == c % n:
			print('Message found!! ', m)
			break
#		m += 1 	
			
	
def find_d(e, phi_n):
	''' This function is used to find the value of d, provided the value of "e" 
		is given. '''
	i = 1
	while True:
#		print(i)
		if (e * i) % phi_n == 1:
			break
		i += 1 
	print('Value of d: ', i)
	return i


def decrypt(d, c, n):
	''' The decryption formula: M = C^d mod n '''
	d = int((c ** d) % n)
	return d


def main():
	try:
	# Handling exceptions if user does not input a valid choice
		choice = int(input('1. Factorization. \n2. Brute-Force \nSelect your Choice: '))
		if not 1 <= choice <= 2:
			raise
	except:
		print(colored('Please enter a valid choice!', 'red'))
		exit(0)
		
	try:
	# Handling exceptions if user does not input valid values for e, n and c.
		e = int(input('Enter the value of e: ')) 
		n = int(input('Enter the value of n: ')) 
		c = int(input('Enter the value of c: ')) 
	except:	
		print(colored('Please enter a valid input!', 'red'))
		exit(0)
	
	if choice == 1:	
		# Start time is the variable used to measure time, in order to find execution time.
		start_time = time.time()
		p, q = find_p_q(e, n)
		
		phi_n = (p-1) * (q-1)
		
		d = find_d(e, phi_n)
		
		plain = decrypt(d, c, n)
		print('Plain text message: ', plain)
		
		# Printing the final time to find the execution time of the program.
		print(colored('Time taken -- {}'.format(time.time() - start_time), 'green'))
		
	else: 
		start_time = time.time()
		brute_force(e, c, n)	
		print(colored('Time taken -- {}'.format(time.time() - start_time), 'green'))
		

if __name__ == '__main__':
	main()


