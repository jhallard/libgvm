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

All of the above scripts can be called with the `-h` option to print a usage statement.

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
cmod +x config.py && ./config.py
```

There isn't much to configure, it will just ask you for your project name and to set a directory or two.

####License
MIT

[GoogleCloudSDK]:https://cloud.google.com/sdk/

