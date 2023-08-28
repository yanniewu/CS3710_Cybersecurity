# Yannie Wu, ylw4sj
# CS 3710 Homework: Cryptocurrency
import binascii, hashlib, rsa, sys, os
from datetime import datetime

# gets the hash of a file; from https://stackoverflow.com/a/44873382
def hashFile(filename):
    h = hashlib.sha256()
    with open(filename, 'rb', buffering=0) as f:
        for b in iter(lambda : f.read(128*1024), b''):
            h.update(b)
    return h.hexdigest()

# given an array of bytes, return a hex reprenstation of it
def bytesToString(data):
    return binascii.hexlify(data)

# given a hex reprensetation, convert it to an array of bytes
def stringToBytes(hexstr):
    return binascii.a2b_hex(hexstr)

# Load the wallet keys from a filename
def loadWallet(filename):
    with open(filename, mode='rb') as file:
        keydata = file.read()
    privkey = rsa.PrivateKey.load_pkcs1(keydata)
    pubkey = rsa.PublicKey.load_pkcs1(keydata)
    return pubkey, privkey

# save the wallet to a file
def saveWallet(pubkey, privkey, filename):
    # Save the keys to a key format (outputs bytes)
    pubkeyBytes = pubkey.save_pkcs1(format='PEM')
    privkeyBytes = privkey.save_pkcs1(format='PEM')
    # Convert those bytes to strings to write to a file (gibberish, but a string...)
    pubkeyString = pubkeyBytes.decode('ascii')
    privkeyString = privkeyBytes.decode('ascii')
    # Write both keys to the wallet file
    with open(filename, 'w') as file:
        file.write(pubkeyString)
        file.write(privkeyString)
    return

########################################################################################

# Print the name of the cryptocurrency
def name():
	print('SandDollar(TM)')

# Create the genesis block
def genesis():
	f = open('block_0.txt', 'w')
	f.write('We all live in a yellow submarine')
	f.close()
	print('Genesis block created in \'block_0.txt\'')

# Generate wallet
def generate(walletName):
	pubkey, privkey = rsa.newkeys(1024)
	saveWallet(pubkey, privkey, walletName)
	print('New wallet generated in \'' + walletName  + '\' with tag ' + hashFile(walletName)[:16])

# Get wallet tag
def address(walletName):
	print(hashFile(walletName)[:16])

# Add funds to wallet
def fund(destTag, amount, filename):
	# Create transaction statement
	with open(filename, 'w') as f:
		f.write('From: Kanye\n')
		f.write('To: ' + destTag + '\n')
		f.write('Amount: ' + amount + '\n')
		f.write('Date: ' + str(datetime.now()))
	
	print('Funded wallet \'' + destTag + '\' with ' + amount + ' SandDollars on ' + str(datetime.now()))

# Transfer money from one wallet to another
def transfer(sourceName, destTag, amount, filename):
	# Create transaction statement
	f = open(filename, 'w')
	transferState = 'From: ' + str(hashFile(sourceName)[:16]) + '\n' + 'To: ' + destTag + '\n' + 'Amount: ' + amount + '\n' + 'Date: ' + str(datetime.now()) + '\n'	
	privkey = loadWallet(sourceName)[1]
	signature = rsa.sign(transferState.encode(), privkey, 'SHA-256')
	signature = binascii.hexlify(signature).decode('utf-8') # Make signature writable to file
	f.writelines([transferState, signature])
	
	print('Transfered ' + amount + ' from ' + sourceName + ' to ' + destTag + ' and the statement to ' + filename + ' on ' + str(datetime.now()))

# Check wallet balance
def balance(walletTag):
	balance = 0

	# Check mempool
	f = open('mempool.txt', 'r')
	for line in f:
		lineArray = line.rsplit(' ')
		if lineArray[0] == walletTag:
			balance -= int(lineArray[2])
		if lineArray[4] == walletTag:
			balance += int(lineArray[2])

	# Check block chain
	blockCounter = 1
	blockName = 'block_' + str(blockCounter) + '.txt'
	while os.path.isfile(blockName):
		f = open(blockName, 'r')
		for line in f:
			lineArray = line.rsplit(' ')
			if len(lineArray) != 8: # Skip hash, nonce, and blank lines
				continue		
			if lineArray[0] == walletTag: 		# Check for deposits
				balance -= int(lineArray[2])
			if lineArray[4] == walletTag: 		# Check for withdrawals
				balance += int(lineArray[2])
		blockCounter += 1
		blockName = 'block_' + str(blockCounter) + '.txt'
	print(balance)
	
# Verify transaction statements and post to mempool
def verify(walletName, transactionFile):
	walletName = sys.argv[2]
	transactionFile = sys.argv[3]

	# Read transactions statement
	with open(transactionFile, 'r') as f:
		lines = f.readlines()
	source = lines[0].strip()[6:]
	dest = str(lines[1].strip())[4:]
	amount = lines[2].strip()[8:]
	date = str(lines[3]).strip()[7:]
	statement = lines[0] + lines[1] + lines[2] + lines[3]

	# Approve all funding requests
	if source == 'Kanye':
		m = open('mempool.txt', 'a')
		m.write(source + ' transferred ' + amount + ' to ' + dest + ' on ' + date + '\n')
		m.close()
		print('Any funding request is considered valid; written to the mempool')
	
	# Verify transfer requests
	else:
		pubkey = loadWallet(walletName)[0]
		signature = lines[4]
		signature = binascii.unhexlify(signature.encode('utf-8'))
		checkSig = rsa.verify(statement.encode(), signature, pubkey)

		if (balance(str(source)) >= int(amount)) and (checkSig == 'SHA-256'):
			m = open('mempool.txt', 'a')
			m.write(source + ' transferred ' + amount + ' to ' + dest + ' on ' + date + '\n')
			m.close()
			print('The transaction in file \'' + transactionFile + '\' with wallet \'' + walletName + '\' is valid; written to the mempool')

# Mine new block
def mine(difficulty):
	blockCounter = 1
	newBlock = 'block_' + str(blockCounter) + '.txt'
	while os.path.isfile(newBlock):
		blockCounter += 1
		newBlock = 'block_' + str(blockCounter) + '.txt'

	# Clear mempool
	with open('mempool.txt', 'r+') as m:
		mempool = m.readlines()
		m.truncate(0)
	m.close()
	nonce = 0

	# Create new block
	with open(newBlock, 'w') as b:
		b.write(hashFile('block_' + str(blockCounter-1) + '.txt') + '\n\n')
		for line in mempool:
			b.write(line)
		b.write('Nonce: ' + str(nonce))

	# Calculate nonce
	while str(hashFile(newBlock))[:int(difficulty)] != ('0' * int(difficulty)):
		nonce += 1
		with open(newBlock, 'w') as b:
			b.write(hashFile('block_' + str(blockCounter-1) + '.txt') + '\n\n')
			for line in mempool:
				b.write(line)
			b.write('Nonce: ' + str(nonce))

	print('Mempool transactions moved to ' + newBlock + ' and mined with difficulty ' + str(difficulty) + ' and nonce ' + str(nonce))

# Validate existing block chain
def validate():
	blockCounter = 1
	blockName = 'block_' + str(blockCounter) + '.txt'
	isValid = True

	while os.path.isfile(blockName):
		currBlock = open(blockName, 'r')
		if currBlock.readline().strip() != hashFile('block_' + str(blockCounter-1) + '.txt'):
			isValid = False
		blockCounter += 1
		blockName = 'block_' + str(blockCounter) + '.txt'
	print(isValid)


if __name__ == '__main__':
    args = sys.argv
    globals()[args[1]](*args[2:])