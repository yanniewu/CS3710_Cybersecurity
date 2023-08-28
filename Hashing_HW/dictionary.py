#!/usr/bin/python3

# Yannie Wu, ylw4sj
# CS 3710 Homework: Hashing (Task 2: Dictionary Attacks)

import sys
import hashlib

def main():

	salt = sys.argv[3]

	# Read password file
	pass_dict = {}
	f = open(sys.argv[2], "r") 
	
	while True:
		line = f.readline()

		if line:
			pass_dict[(line.split()[1])] = line.split()[0]; # pass_dict[hash] = name
		else:
			break

	f.close()

	# Read words file
	words_dict = {}
	f = open(sys.argv[1], "r")
	
	while True:
		word = f.readline().strip()
		
		if word:
			sha256hash = str(hashlib.sha256(bytes(word + salt,"ascii")).hexdigest())
			words_dict[sha256hash] = word   # word_dict[hash] = word
		else:
			break

	f.close()

	# Match hash with passwords
	for key in pass_dict:
		name = pass_dict[key]
		cracked_pass = words_dict[key]
		print("password for " + name + " is: " + cracked_pass)


if __name__ == '__main__':
	main()

