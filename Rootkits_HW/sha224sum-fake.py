#!/usr/bin/python3

# Yannie Wu, ylw4sj
# Programming HW: Rootkits (Part 3: Wrapper files)

import sys, os

def main():

	is_evil = False 
	sha_flags = ''
	filename = ''
	
	if len(sys.argv) > 1:
		filename = sys.argv[1] # File to be hashed

	# Check for other command-line parameters
	i = 2 
	while i < len(sys.argv): 	
		if sys.argv[i] == '--be-evil':
			is_evil = True
		else:
			sha_flags += (' ' + sys.argv[i])
		i += 1

	# Print quote
	if is_evil:
		print('Get in loser.\nWe\'re going shopping.')
	else:
		print('That is so fetch')

	# Call sha244sum.original
	os.system('/usr/bin/sha224sum.original ' + filename + sha_flags)

if __name__ == '__main__':
	main()