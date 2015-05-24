#!/usr/bin/env python
import sys
import subprocess
from util import *
from sys import stdin

def print_help() :
	print "This lets you login to a current VM instance"
	print "Usage : login.py [-h] instance_name"


if __name__ == "__main__":

	opts = get_opts(sys.argv)
	defs = {}
	args = sys.argv[len(opts):]

	if "help" in opts :
		print_help()
		sys.exit(0)

# if a name is specified as an arg
	if len(args) >= 2 :
		content = [line.strip() for line in open(INSTANCE_FN)]
		for line in content :
			if line.split()[0] == args[0]:
				subprocess.call(['gcloud','compute','ssh', instance_name, '--zone', line.split()[1]])
				sys.exit(0)       

	else :
		content = [line.strip() for line in open(INSTANCE_FN)]
		i = 1

		# if there is nothing in the file we need to enter all info manually
		if len(content) == 0 :
			print "No stored instances in current_instances \n " + \
			" Please manually enter an instance name "
			instance_name = stdin.readline()
			zone = get_zone()
			subprocess.call(['gcloud','compute','ssh', instance_name, '--zone', zone])
			sys.exit(0)

		pair = get_instance_pair()
		instance_name = pair[0]
		zone = pair[1]
		subprocess.call(['gcloud','compute','ssh', instance_name, '--zone', zone])
		sys.exit(0)



