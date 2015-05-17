#!/usr/bin/env python
import sys
import subprocess
from sys import stdin
from util import *

SCOPE1 = "https://www.googleapis.com/auth/devstorage.read_write"
SCOPE2 = "https://www.googleapis.com/auth/logging.write"

def print_help() :
	print "This deletes an existing snapshot"
	print "Usage : remove_snapshot.py [-h -d] snapshot_name project_name"
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
      
	if len(args) >= 2 :
		snapshot_name = args[1]
		names = get_snapshot_names()

		if snapshot_name not in names :
			print "Snapshot Name Does Not Exists (argv[1]) \n"
			print "Current Names are : \n"
			for x in names :
				print x
			sys.exit(1)

	else :
		snapshot_name = get_snapshot_name()
	
	# get project name
	if project == "" and len(args) >= 3 :
		project = args[2]

	elif project == "" :
		project = select_project_name()
	

	try :

		ret = subprocess.check_output(['gcloud','compute','snapshots', 'delete', snapshot_name,
		 '--project', project ])

		update_snapshot_list()

	except subprocess.CalledProcessError, e:
		print "Error : Failed to Delete Snapshot \n" + str(e)



