from operator import xor
from termcolor import colored

def left_shifts(data, shift_count):
	'''Used for bit operation - left shift.
	The characters corresponding to the left shift are appended to the right part of the string'''
	return(data[shift_count:] + data[:shift_count])
		
def get_subkeys(key):
	'''This is used for left shifts of key'''
	subkey1 = left_shifts(key[:5], 1) + left_shifts(key[5:], 1)
	subkey2 = left_shifts(subkey1[:5], 2) + left_shifts(subkey1[5:], 2)
	return subkey1, subkey2
	
def permutate_keys(key, permutate):
	'''Used for P4, P8 and P10'''
	p4 = [1, 3, 2, 0]
	p8 = [5, 2, 6, 3, 7, 4, 9, 8]
	p10 = [2, 4, 1, 6, 3, 9, 0, 8, 7, 5]
	result = []
	if permutate == 8:
		result = [key[i] for i in p8]
	elif permutate == 10:
		result = [key[i] for i in p10]
	elif permutate == 4:
		result = [key[i] for i in p4]
	return result
	
# 0: IP, 1: IP inverse, 2: Expand and permutate
def permutate_plain_text(text, permutate):
	'''The IP, IP inverse and Expand & permutate operation'''
	init_permute = [1, 5, 2, 0, 3, 7, 4, 6]
	init_permute_inverse = [3, 0, 2, 4, 6, 1, 7, 5]
	ep = [3, 0, 1, 2, 1, 2, 3, 0]
	result = []
	if permutate == 0:
		result = [text[i] for i in init_permute]
	elif permutate == 1:
		result = [text[i] for i in init_permute_inverse]
	elif permutate == 2:
		result = [text[i] for i in ep]
	return result

def sbox_lookup(row, column):
	'''Used to lookup for values in S-boxes, since not performing bit operations'''
	if row == 0 and column == 0:
		return 0
	elif row == 0 and column == 1:
		return 1
	elif row == 1 and column == 0:
		return 2
	elif row == 1 and column == 1:
		return 3
		
def sbox_lookup_return(value):
	'''The lookup of values retrieved, since not performing bit operations'''
	if value == 0:
		return [0, 0]
	elif value == 1:
		return [0, 1]
	elif value == 2:
		return [1, 0]
	elif value == 3:
		return [1, 1]

def sbox_in_use(sbox_choice):
	'''To check whether the user wants to use modified Sbox or not. True is "Yes" and False is "NO" '''
	if sbox_choice == 'y':
		return True
	return False
	

def apply_sbox(result_xor, mod_sbox):
	'''This function is used for appling SBox to the output of XOR of EP and keys'''
	s0_data = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
	s1_data = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]
	mod_s1_data = [[2, 1, 0, 3], [2, 0, 1, 3], [3, 0, 1, 0], [0, 1, 2, 3]]

	s0_value1 = sbox_lookup(result_xor[0], result_xor[3])
	s0_value2 = sbox_lookup(result_xor[1], result_xor[2])
	s0_final = sbox_lookup_return(s0_data[s0_value1][s0_value2])

	s1_value1 = sbox_lookup(result_xor[4], result_xor[7])
	s1_value2 = sbox_lookup(result_xor[5], result_xor[6])
	
	if mod_sbox == True:
		s1_final = sbox_lookup_return(mod_s1_data[s1_value1][s1_value2])	
	else:	
		s1_final = sbox_lookup_return(s1_data[s1_value1][s1_value2])
	
	return s0_final + s1_final


def apply_cryptography(process_text, key1, key2, mod_sbox, encryption):
	'''Function used for encryption and decryption. If the encryption parameter is true, it will encrypt
		if the encryption parameter is false, it will decrypt.'''
		
	swap = [] # Used to store the intermediate values. Since using for loop, the first value is selected.
	for i in range(2):
		# Splitting the PT(IP) in left and right for operation.
		left = process_text[:4]
		temp_right = process_text[4:]
		right = permutate_plain_text(process_text[4:], 2)
		
		# XOR the EP output to the keys
		if encryption == True:
			if i == 0:
				result_xor = [(xor(int(a), int(b))) for a, b in zip(right, key1)]
			else:
				result_xor = [(xor(int(a), int(b))) for a, b in zip(right, key2)]
		else:
			if i == 0:
				result_xor = [(xor(int(a), int(b))) for a, b in zip(right, key2)]
			else:
				result_xor = [(xor(int(a), int(b))) for a, b in zip(right, key1)]

		s_final = apply_sbox(result_xor, mod_sbox)

		right = (permutate_keys(s_final, 4))
		
		# The output of P4 is XORed with left, and appended as the left portion of the process text.
		sbox_output = [(xor(int(a), int(b))) for a, b in zip(right, left)] + temp_right
		
		# Swapping the left and right 4 bits
		process_text = (left_shifts(sbox_output, 4))
		swap.append(process_text) # The intermediate values stored.
	
	return_text = permutate_plain_text(sbox_output, 1) # Applying IP inverse to the final string
	return swap[0], return_text	# Returning the intermediate and Cipher/Retrieved Plain Text

'''-----------------------------------Input from User--------------------------------'''
try:
	user_key = list(map(int, input('Enter a 10 bit space-separated key: ').split()))
	process_text = permutate_plain_text(list(map(int, input('Enter an 8 bit space-separated plain text: ').split())), 0)
	sbox_choice = sbox_in_use(input('Do you want to use the modified s1 Box? (y/n): '))
	
	if len(user_key) != 10 or len(process_text) != 8:
		raise
# Handling exceptions occured on input!
except:
	print(colored('Please enter valid input!!', 'red'))
	exit(0)


# The P10 is applied to the keys on taking the input
key1, key2 = get_subkeys(permutate_keys(user_key, 10))

# Applying p8 to the keys to get the final subkeys
key1 = permutate_keys(key1, 8)
key2 = permutate_keys(key2, 8)

'''-----------------------------------------------Encryption and decryption-------------------------------------'''
intermediate, cipher_text = apply_cryptography(process_text, key1, key2, sbox_choice, encryption=True)
print('\nIntermediate Text: ', intermediate)
print('\nCipher Text: ', cipher_text)
intermediate, plain_text = apply_cryptography(permutate_plain_text(cipher_text, 0), key1, key2, sbox_choice, encryption=False)
print('\nIntermediate text: ', intermediate)
print('\nPlain Text: ', plain_text)

