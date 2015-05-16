#!/usr/bin/env python
import sys
import subprocess
from sys import stdin
from util import *

SCOPE1 = "https://www.googleapis.com/auth/devstorage.read_write"
SCOPE2 = "https://www.googleapis.com/auth/logging.write"

def print_help() :
	print "This creats a new VM instance from scratch using a " + \
	"boot image OS provided by Google."
	print "Usage : make_new_instance.py [-h] instance_name machine_type zone startup_script boot_image"


if __name__ == "__main__":
	instance_name = ""
	machine_type = ""
	zone = ""
	script = ""
	boot_image = ""

	if len(sys.argv) >= 2 and sys.argv[1] in ["-h", "-help", "help"] :
		print_help()
		sys.exit(0)

	# if a name is specified as an arg
	if len(sys.argv) >= 2 :
		instance_name = sys.argv[1]
		instances = get_instance_names()

		if instance_name in instances :
			print "Instance Already Exists, Try Again"
			sys.exit(1)
	else :
		instance_name = get_new_instance_name()
      
	if len(sys.argv) >= 3 :
		machine_type = sys.argv[2]
		types = get_machine_names()

		if machine_type not in types :
			print "Invalid Machine Type (argv[2]) \n"
			print "Valid Types are : \n"
			for x in types :
				print x
			sys.exit(1)

	else :
		machine_type = get_machine_type()
	
	if len(sys.argv) >= 4 :
		zone = sys.argv[3]
		zones = get_zone_names()

		if zone not in zones :
			print "Invalid Zone Entry (argv[3]) \n"
			print "Valid Zones are : \n"
			for x in zones :
				print x
			sys.exit(1)
	else :
		zone = get_zone()

	if len(sys.argv) >= 5 :
		script = sys.argv[4]
		scripts = get_startup_script_names()

		if script not in scripts :
			print "Invalid Script Entry (argv[4]) \n"
			print "Valid Scripts are : \n"
			for x in scripts :
				print x
			sys.exit(1)
	else :
		script = get_startup_script()


	if len(sys.argv) >= 6 :
		image = sys.argv[5]
		images = get_boot_image_names()

		if image not in images :
			print "Invalid Boot Image Entry (argv[5]) \n"
			print "Valid Images are : \n"
			for x in images :
				print x
			sys.exit(1)
	else :
		image = get_boot_image()


	try :

		if script == "" :
			ret = subprocess.check_output(['gcloud','compute','--project', PROJECT_NAME, 'instances', 'create',
				instance_name, '--zone', zone, '--machine-type', machine_type, '--network', 'default',
				'--maintenance-policy', 'MIGRATE', '--scopes='+SCOPE1+','+SCOPE2, '--tags=http-server,https-server',
				'--image', image, '--boot-disk-type', 'pd-standard', '--boot-disk-device-name', instance_name])
		else :
			ret = subprocess.check_output(['gcloud','compute','--project', PROJECT_NAME, 'instances', 'create', instance_name,
				'--metadata-from-file','startup-script='+script, '--zone', zone, '--machine-type', machine_type,
				'--network', 'default', '--maintenance-policy', 'MIGRATE', '--scopes='+SCOPE1+','+SCOPE2, 
				'--tags=http-server,https-server', '--image', image, '--boot-disk-type', 'pd-standard',
				'--boot-disk-device-name', instance_name])

		# update the file that keeps track of instances
		update_instances_list()

	except subprocess.CalledProcessError, e:

		print "Error : Failed to Start Instance \n" + str(e)



