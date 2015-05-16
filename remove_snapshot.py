#!/usr/bin/env python
import sys
import subprocess
from sys import stdin
from util import *

SCOPE1 = "https://www.googleapis.com/auth/devstorage.read_write"
SCOPE2 = "https://www.googleapis.com/auth/logging.write"

def print_help() :
	print "This deletes an existing snapshot"
	print "Usage : remove_snapshot.py [-h] snapshot_name"

if __name__ == "__main__":
	instance_name = ""
	snapshot_name = ""
	zone = ""
	machine_type = ""

	if len(sys.argv) >= 2 and sys.argv[1] in ["-h", "-help", "help"] :
		print_help()
		sys.exit(0)
      
	if len(sys.argv) >= 2 :
		snapshot_name = sys.argv[1]
		names = get_snapshot_names()

		if snapshot_name not in names :
			print "Snapshot Name Does Not Exists (argv[1]) \n"
			print "Current Names are : \n"
			for x in names :
				print x
			sys.exit(1)

	else :
		snapshot_name = get_snapshot_name()
	

	try :

		snapshot_path="https://www.googleapis.com/compute/v1/projects/"
		snapshot_path+=PROJECT_NAME
		snapshot_path+="/zones/us-central1-b/disks/"
		snapshot_path+=instance_name
		ret = subprocess.check_output(['gcloud','compute','snapshots', 'delete', snapshot_name,
		 '--project', PROJECT_NAME ])

		# out = ret.split('\n')[1]
		# with open(SNAPSHOT_FN, "a") as myfile:
		#     myfile.write(snapshot_name + " " + zone + '\n')
		# sys.exit(0)

		update_snapshot_list()

	except subprocess.CalledProcessError, e:
		print "Error : Failed to Delete Snapshot \n" + str(e)



