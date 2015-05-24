#!/usr/bin/env python
import sys
import subprocess
from sys import stdin
from util import *

SCOPE1 = "https://www.googleapis.com/auth/devstorage.read_write"
SCOPE2 = "https://www.googleapis.com/auth/logging.write"

def print_help() :
	print "This creates a new snapshot of an existing VM instance"
	print "Usage : make_snapshot.py [-h -d] instance_name snapshot_name project_name"
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
      
	if len(args) >= 3 :
		snapshot_name = args[2]
		names = get_snapshot_names()

		if snapshot_name in names :
			print "Snapshot Name Already Exists (argv[2]) \n"
			print "Current Names are : \n"
			for x in names :
				print x
			sys.exit(1)

	else :
		snapshot_name = get_new_snapshot_name()

	print "Please Enter a Snapshot Description : \n"
	desc = stdin.readline()

		# get project name
	if project == "" and len(args) >= 4 :
		project = args[2]

	elif project == "" :
		project = select_project_name()
	

	try :

		snapshot_path="https://www.googleapis.com/compute/v1/projects/"
		snapshot_path+=PROJECT_NAME
		snapshot_path+="/zones/"+zone+"/disks/"
		snapshot_path+=instance_name
		ret = subprocess.check_output(['gcloud','compute','--project', PROJECT_NAME,
			'disks', 'snapshot', snapshot_path, '--description', desc, '--zone', zone,
			'--snapshot-names', snapshot_name])

		# out = ret.split('\n')[1]
		# with open(SNAPSHOT_FN, "a") as myfile:
		#     myfile.write(snapshot_name + " " + zone + '\n')
		# sys.exit(0)

		update_snapshot_list()

	except subprocess.CalledProcessError, e:
		print "Error : Failed to Create Snapshot" + instance_name +"\n"+ str(e)



