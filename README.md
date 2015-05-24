# LibGVM

This is a simple library of python scripts to simplify the creation, use, and deletion of virtual-machine through the Google Compute Engine.
Inside the `/data/` directory are a few files which keep track of instances, snapshots, and VM options. They are :
* `/data/current_instances` - List of current instance names, zones, local IPs, and external IPs.
* `/data/current_snapshots` - List of existing snapshot names.
* `/data/zones` - Valid zone names for Google Compute Engine.
* `/data/machine_types` - Valid machine type names for GCE.
* `/data/boot_images` - Default boot-image names provided by GCE

It also contains all of the zone and machine-type names for quick selection when making new VM instances. The scripts included are :

* `login.py` - Presents a list of running VMs and lets the user select one to login to.
* `make_new_instance.py` - Make a new instance from a standard Google-supplied OS-image (like Ubuntu or Debian), also can supply a local start-up script.
* `make_new_instance_snapshot.py` - Make a new instance from a saved VM snapshot.
* `make_snapshot.py` - Make a snapshot of a current running VM instance.
* `remove_instance.py` - Delete a running VM instance, gives the opportunity to make a snapshot before deleting.
* `remove_snapshot.py` - Delete a saved VM snapshot.

#### Startup-scripts

Simply place any startup scripts you need in the `/startup_scripts/` directory, then when you try to use one when calling `make_new_instance.py` a list of startup scripts from that directory will be presented to you to choose from.

##### Get LibGVM
To start, you will need to install the [GoogleCloudSDK]
```sh
# Open a terminal [ctrl-shift-t]
curl https://sdk.cloud.google.com | bash
# Restart the terminal
gcloud auth login # Enter you Google Developer Credentials
gcloud config set project $PROJECT_NAME # *optional* but convenient if you're only working on one project
```

Now you can clone this project and configure
```sh
git clone https://github.com/jhallard/libgvm.git
cd libgvm.git
cmod +x config.sh && ./config.sh
```

The configuration will allow you to set some default values for the library, note that these defaults are only used if a script is called with the `-d` option. The defaults are as follows :
* zone - Set the default region (us-central1, asia-east1, etc) for all future vm creations.
* machine type - Set the default machine type (n1-standard, g1-small, etc.).
* boot image - Set the default OS boot image (ubuntu 15.04, Debian-7, etc.).
* projects - Set the list of project names that belong to you through Google Developers Console. If only one is set that one will be auto selected with the `-d` option.

##### Options
* `-h` - Prints a usage statement of deccription of the program.
* `-d` - Uses any default values it can load from the default files stored in `/data/`

The default values it can load are zone, machine type, boot-image, and project name. Instance names and snapshot names must be entered manually in-script or as arguments.


####License
MIT

[GoogleCloudSDK]:https://cloud.google.com/sdk/

