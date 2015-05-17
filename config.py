#!/usr/bin/env python
import sys
import subprocess
from util import *
from sys import stdin

def print_help() :
	print "This lets you configure the default settings for libgvm"
	print "This includes setting the projects you're working on, the default vm zone, default machine type, and default boot-image"
	print "Usage : config.py [-h]"


def set_default_zone() :
	conf = get_confirm("Would you like to set a default zone?")
	if not conf :
		return

	zone = get_zone()
	f = open(DEFAULT_ZONE_FN, 'wr+')
	f.seek(0)
	f.write(zone)
	f.truncate()
	f.close()

def set_default_machine() :
	conf = get_confirm("Would you like to set a default machine-type?")
	if not conf :
		return

	machine = get_machine_type()
	f = open(DEFAULT_MACHINE_FN, 'wr+')
	f.seek(0)
	f.write(machine)
	f.truncate()
	f.close()

def set_default_boot_image() :
	conf = get_confirm("Would you like to set a default OS boot-image?\n (note that this won't apply if you start from a custom snapshot")
	if not conf :
		return

	image = get_boot_image()
	f = open(DEFAULT_BOOT_FN, 'wr+')
	f.seek(0)
	f.write(image)
	f.truncate()
	f.close()

def set_project() :
	conf = get_confirm("Would you like to set a list of Google Developer project you are working on? \n If you set only one it will be used as default with the -d command, with more than one you will be prompted to select.")
	if not conf :
		return
	
	inp = ""
	print "Please enter the project names, seperated by commas"

	while inp == "" :
		inp = stdin.readline()

	parts = inp.split(',')
	parts = [x.strip() for x in parts]

	f = open(DEFAULT_PROJECT_FN, 'wr+')
	f.seek(0)
	for p in parts :
		f.write(str(p)+'\n')
	f.truncate()
	f.close()

if __name__ == "__main__":
	print "LibGVM : Config"
	print "None of the following values need to be set, but setting the defaults allows you to more efficiently"
	print "operate your virtual machines. \n\n"
	set_default_zone()
	set_default_machine()
	set_default_boot_image()
	set_project()