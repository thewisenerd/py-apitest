import os
import functools

from termcolor import colored

print = functools.partial(print, end='', flush=True)

def nukeline():
	# nukes everything in line and moves cursor to beginning
	print("\033[2K\r")

def info(s):
	print('[ %s ] %s' % (colored('…', 'blue'), colored(s, 'white')));

def success(s):
	print('[ %s ] %s' % (colored('✓', 'green'), colored(s, 'white')));

def error(s):
	print('[ %s ] %s' % (colored('✕', 'red'), colored(s, 'white')));

# thanks ghostdog74
# https://stackoverflow.com/a/3964691
def findfilesendingwith(endstr, basedir):
	for root, dirs, files in os.walk(basedir):
		for file in files:
			if file.endswith(endstr):
				yield (os.path.join(root, file))
