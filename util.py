#!/usr/bin/env python
import sys
import os
import subprocess
from os import listdir
from os.path import isfile, join
from sys import stdin

INSTANCE_FN = "data/current_instances"
SNAPSHOT_FN = "data/current_snapshots"
MACHINE_FN = "data/machine_types"
ZONE_FN = "data/zones"
STARTUP_FN = "startup_scripts"
PROJECT_NAME = "" # TODO implement config to set PROJECT_NAME
BOOT_IMAGES_FN = "data/boot_images"

def is_non_empty_file(fpath):  
    return True if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else False

# return all instance names, only names
def get_instance_names() :
	if is_non_empty_file(INSTANCE_FN) :
		return [line.strip().split()[0] for line in open(INSTANCE_FN) if line.strip() != ""]
	else :
		return []
		
# returns pairs of [instance_name, instance_zone] for all instances 
def get_instance_pairs() :
	if is_non_empty_file(INSTANCE_FN) :
		return [[line.strip().split()[0], line.strip().split()[1]] for line in open(INSTANCE_FN) if line.strip() != ""]
	else :
		return []
		
# return all instance names, only names
def get_full_instance_names() :
	if is_non_empty_file(INSTANCE_FN) :
		return [line.strip() for line in open(INSTANCE_FN)]
	else :
		return []
		
# return all snapshot names
def get_snapshot_names() :
	if is_non_empty_file(SNAPSHOT_FN) :
		return [line.strip() for line in open(SNAPSHOT_FN)]
	else :
		return []

# return all zone names
def get_zone_names() :
	return [line.strip() for line in open(ZONE_FN)]

# return all zone names
def get_machine_names() :
	return [line.strip() for line in open(MACHINE_FN)]

# return all instance names, only names
def get_startup_script_names() :
	return [ f for f in listdir(STARTUP_FN) if isfile(join(STARTUP_FN,f)) ]

# returns a list of all of the OS iamges for booting
def get_boot_image_names() :
	return [line.strip() for line in open(BOOT_IMAGES_FN)]

# removes a single instance reference from the file (deprecated)
def remove_instance_from_file(instance_name) :
	f = open(INSTANCE_FN,"r+")
	d = f.readlines()
	f.seek(0)
	for i in d:
	    if i.split()[0].strip() != instance_name:
	        f.write(i)
	f.truncate()
	f.close()


# updates the list of current instances
def update_instances_list() :
	ret = subprocess.check_output(['gcloud', 'compute', 'instances', 'list'])
	ret = ret.split('\n')
	f = open(INSTANCE_FN, 'r+')
	f.seek(0)

	for line in ret[1:] :
		f.write(line+'\n')
	f.truncate()
	f.close()

# updates the list of current instances
def update_snapshot_list() :
	ret = subprocess.check_output(['gcloud', 'compute', 'snapshots', 'list'])
	ret = ret.split('\n')
	f = open(SNAPSHOT_FN, 'r+')
	f.seek(0)

	if len(ret) >= 2 :
		for line in ret[1:] :
			if len(line) > 0 :
				name = line.strip().split()[0]
				# zone = line.split()[2].split('/')[0]
				f.write(name+'\n')
	f.truncate()
	f.close()



# prints the list of available zones for choosing and returns
# the selected one
def get_zone() :
	zones = get_zone_names()
	i = 1
	print "Please Select a Zone Number : \n"

	for line in zones :
		print str(i) + " : " + line
		i = i+1
	num = -1
	while num <= 0 or num >= (i) :
		num = int(stdin.readline())

	return zones[num-1]

# prints the list of available zones for choosing and returns
# the selected one
def get_machine_type() :
	machines = get_machine_names()
	i = 1
	print "Please Select a Machine Number : \n"

	for line in machines :
		print str(i) + " : " + line
		i = i+1
	num = -1
	while num <= 0 or num >= (i) :
		num = int(stdin.readline())

	return machines[num-1]

# prints the list of available zones for choosing and returns
# the selected one
def get_boot_image() :
	images = get_boot_image_names()
	i = 1
	print "Please Select a Boot Image Number : \n"

	for line in images :
		print str(i) + " : " + line
		i = i+1
	num = -1
	while num <= 0 or num >= (i) :
		num = int(stdin.readline())

	return images[num-1].strip()

# prints the list of available instances and their zones for choosing and returns
# the selected pair {instance-name, zone}
def get_instance_pair() :
	instances = get_instance_pairs()
	i = 1

	print "Please Select a Instance Number : \n"
	for line in instances :
		print str(i) + " : " + line[0]
		i = i+1
	num = -1
	while num <= 0 or num >= (i) :
		num = int(stdin.readline())

	return [instances[num-1][0], instances[num-1][1]]

# prints all of the snapshot names and lets the user select one
# to make a new instance from
def get_snapshot_name() :
	names = get_snapshot_names()
	i = 1

	print "Please Select a Snapshot Number : \n"
	for line in names :
		print str(i) + " : " + line
		i = i+1
	num = -1
	while num <= 0 or num >= (i) :
		num = int(stdin.readline())

	return names[num-1].strip()

# prints the list of available startup scripts for choosing and returns
# the selected one
def get_startup_script() :
	scripts = get_startup_script_names()
	i = 1
	print "Please Select a Startup-Script Number : \n"

	for line in scripts :
		print str(i) + " : " + line
		i = i+1
	print str(i) + " : Don't use a Script \n" # give the option to use no script

	num = -1
	while num <= 0 or num > (i) :
		num = int(stdin.readline())

	if num == i :
		return ""

	return os.getcwd() + "/" + STARTUP_FN + "/" + scripts[num-1]

# gets a new instance name from the user while ensuring it does 
# not interfere with an existing instance name
def get_new_instance_name() :

	print "Enter a Name for this Instance : "
	instances = get_instance_pairs()
	instance_names = get_instance_names()
	new_name = ""

	while new_name == "" :
		new_name = stdin.readline().strip()
		if new_name.strip() in instance_names :
			print "Instance Name Alread Exists, Try Again : "
			new_name = ""

	return new_name

# gets a new snapshot name from the user while ensuring it does
# not interfere with an existing snapshot name
def get_new_snapshot_name() :

	print "Enter a Name for this Snapshot : "
	names = get_snapshot_names()
	new_name = ""

	while new_name == "" :
		new_name = stdin.readline().strip()
		if new_name in names :
			print "Snapshot Name Alread Exists, Try Again : "
			new_name = ""

	return new_name