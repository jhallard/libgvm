#!/usr/bin/env python
import sys
import subprocess
from sys import stdin
from util import *

SCOPE1 = "https://www.googleapis.com/auth/devstorage.read_write"
SCOPE2 = "https://www.googleapis.com/auth/logging.write"

def print_help() :
	print "This creats a new VM instance from an existing snapshot"
	print "Usage : remove_instance.py [-h -d] instance_name snapshot_name machine_type zone project_name"
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
		machine_type = defs["machine"]
		zone = defs["zone"]
		boot_image = defs["image"]
		# if they only have one def. project set
		if len(defs["projects"]) == 1 :
			project = defs["projects"][0]

	# if a name is specified as an arg
	if len(args) >= 2 :
		instance_name = sys.argv[1]
		instances = get_instance_names()

		if instance_name.strip() in instances :
			print "Instance Already Exists, Try Again"
			sys.exit(1)
	else :
		instance_name = get_new_instance_name()
      
	if len(args) >= 3 :
		snapshot_name = sys.argv[2]
		names = get_snapshot_names()

		if snapshot_name not in names :
			print "Invalid Snapshot Name (argv[2]) \n"
			print "Valid Names are : \n"
			for x in names :
				print x
			sys.exit(1)

	else :
		snapshot_name = get_snapshot_name()

      
	if machine_type == "" and len(args) >= 4 :
		machine_type = sys.argv[3]
		types = get_machine_names()

		if machine_type not in types :
			print "Invalid Machine Type (argv[2]) \n"
			print "Valid Types are : \n"
			for x in types :
				print x
			sys.exit(1)

	elif machine_type != "":
		machine_type = get_machine_type()

	if zone == "" and len(args) >= 5 :
		zone = sys.argv[4]
		zones = get_zone_names()

		if zone not in zones :
			print "Invalid Zone Entry (argv[3]) \n"
			print "Valid Zones are : \n"
			for x in zones :
				print x
			sys.exit(1)
	elif zone != "" :
		zone = get_zone()

		# get project name
	if project == "" and len(args) >= 6 :
		project = args[5]

	elif project == "" :
		project = select_project_name()
	

	try :
		subprocess.check_output(['gcloud','compute','--project', project, 'disks', 'create', instance_name,
			'--zone', zone, '--source-snapshot', snapshot_name, '--type', 'pd-standard'])

		ret = subprocess.check_output(['gcloud','compute','--project', project, 'instances', 'create',
			instance_name, '--zone', zone, '--machine-type', machine_type, '--network', 'default',
			'--maintenance-policy', 'MIGRATE', '--scopes='+SCOPE1+','+SCOPE2, '--tags=http-server,https-server',
			'--disk', 'name='+instance_name, 'device-name='+instance_name, 'mode=rw', 'boot=yes', 'auto-delete=yes'])

		# update the file that keeps track of instances
		update_instances_list()

	except subprocess.CalledProcessError, e:

		print "Error : Failed to Create New Instance" + instance_name +"\n" + str(e)



