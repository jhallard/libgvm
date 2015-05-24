#!/usr/bin/env python
import sys
import subprocess
from sys import stdin
from util import *

SCOPE1 = "https://www.googleapis.com/auth/devstorage.read_write"
SCOPE2 = "https://www.googleapis.com/auth/logging.write"

def print_help() :
	print "This removes an existing VM instance"
	print "Usage : remove_instance.py [-h -d] instance_name project_name"
	print "-h : prints this help message"
	print "-d : uses whatever default values have been stored by config.sh"

if __name__ == "__main__":
	instance_name = ""
	snapshot_name = ""
	zone = ""
	machine_type = ""
	project = ""

	opts = get_opts(sys.argv)
	defs = {}
	args = sys.argv[len(opts):]

	if "help" in opts :
		print_help()
		sys.exit(0)

	if "default" in opts :
		defs = load_defaults()
		# if they only have one def. project set
		if len(defs["projects"]) == 1 :
			project = defs["projects"][0]

	# if a name is specified as an arg
	if len(args) >= 2 :
		instance_name = args[1]
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

	# get project name
	if project == "" and len(args) >= 3 :
		project = args[2]

	elif project == "" :
		project = select_project_name()
     
	
	
	inp = get_confirm("Would you like to make a snapshot of instance : " + instance_name + " before deleting it?")

	if inp == True :
		path = os.getcwd()+'/make_snapshot.py'
		ret = subprocess.call([path, instance_name])
	else :
		print "No snapshot will be taken"


	try :
		# print instance_name + "\n" + zone + "\n" + project
		ret = subprocess.check_output(['gcloud','compute', 'instances', 'delete',
			instance_name, '--zone', zone, '-q', '--project', project])

		# remove_instance_from_file(instance_name)
		update_instances_list()

	except subprocess.CalledProcessError, e:

		print "Error : Failed to Remove Instance \n" + str(e)



