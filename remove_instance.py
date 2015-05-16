#!/usr/bin/env python
import sys
import subprocess
from sys import stdin
from util import *

SCOPE1 = "https://www.googleapis.com/auth/devstorage.read_write"
SCOPE2 = "https://www.googleapis.com/auth/logging.write"

def print_help() :
	print "This removes an existing VM instance"
	print "Usage : remove_instance.py [-h] instance_name"

if __name__ == "__main__":
	instance_name = ""
	snapshot_name = ""
	zone = ""
	machine_type = ""

	if len(sys.argv) >= 2 and sys.argv[1] in ["-h", "-help", "help"] :
		print_help()
		sys.exit(0)

	# if a name is specified as an arg
	if len(sys.argv) >= 2 :
		instance_name = sys.argv[1]
		instances = get_instance_names()
		pairs = get_instance_pairs()

		if instance_name not in instances :
			print "Instance Name Doesn't Exists, Try Again"
			print "Valid Instance Are : \n"
			for name in instances :
				print name
			sys.exit(1)

		for pair in pairs :
			if pair[0] == instance_name :
				zone = pair[1]
	else :
		(instance_name, zone) = get_instance_pair()
     
	
	
	print "Would you like to make a snapshot of instance : " + instance_name + " before deleting it?"
	inp = stdin.readline().strip()

	if inp == 'y' or inp == 'Y' or inp == 'yes' :
		path = os.getcwd()+'/make_snapshot.py'
		ret = subprocess.call([path, instance_name])
	else :
		print "No snapshot will be taken"


	try :

		ret = subprocess.check_output(['gcloud','compute', 'instances', 'delete',
			instance_name, '--zone', zone, '-q'])

		# remove_instance_from_file(instance_name)
		update_instances_list()

	except subprocess.CalledProcessError, e:

		print "Error : Failed to Start Instance \n" + str(e)



