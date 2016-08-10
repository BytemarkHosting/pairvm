Wiki
====

Overview
--------

`pairvm` is a tool which makes it easy to host KVM virtual machines
across a pair of hosts.

Each host has two LVM2 volume groups. The first named "here" stores the
virtual discs for VMs that normally run locally, and the second "there"
stores the discs of virtual machine running on the other server in the
pair. These disc images are kept synchronised between the pair using
DRBD.

Each server has two IP addresses, one for administration and the other
for DRBD replication. There is a shared pool of IPs for VMs that
`pairvm` manages, accessed via a bridge.

Installation
------------

The code is available from the [mercurial
repository](/projects/pairvm/repository), and we also automatically
build and release Debian packages:

-   http://repo.bytemark.co.uk/pairvm/

Configuration
-------------

Once installed, PairVM has a simple setup wizard launched as follows:

    # pairvm first_time_setup

Before running this the network needs to be configured on both machines.
There are normally three network interfaces, one for administration
(over which PairVM must be able to SSH to the pair machine), one for
replication, and a third for virtual host network access. The PairVM
hosts do not need an IP address on the access network, but this
interface should be added to a bridge called br0.

Here is an example PairVM network configuration:

    # The administrative interface
    auto eth0
    iface eth0 inet static
            address   10.1.0.2
            netmask   255.255.255.0
            broadcast 10.1.0.255
            gateway   10.1.0.1

    # The replication interface
    auto eth1
    iface eth1 inet static
            address   10.2.0.1
            netmask   255.255.255.248
            broadcast 10.2.0.7

    # The VM access interface
    auto vlan1000
    iface vlan1000 inet manual
            vlan-raw-device eth0
            netmask   255.255.255.0
            broadcast 10.3.0.255
            gateway   10.3.0.1 

    auto br0
    iface br0 inet manual
            bridge-ports vlan1000

PairVM stores its configuration files in `/machines`. There is a global
configuration file `/machines/_global` and each VM has
`/machines/<name>`. If it necessary to manually edit any of these files
it is important that the appropriate change is made to the files on both
hosts in the pair. The VM configuration files should be identical on
both hosts, but `_global` is not so careful editing is required.

Usage
-----

The tool should be self-documenting through the "help" command:

    # pairvm help

More detail information is available for each command via:

    # pairvm help 

### Creating and installing VMs

The create command is used to create a new VM.

    # pairvm create myvm here 1024 10G

In this example a new VM called `myvm` is created with 1GiB RAM and
10GiB disc. An IP address is automatically allocated from the pool.

There are two options for installing a guest operating system. Either
insert a CD/DVD:

    # pairvm cdrom myvm RebeccaBlackLinux.iso

or use Bytemark's OS image servers:

    # pairvm image myvm squeeze password123

### Controlling VMs

These commands should be run the VM's "home" machine.

The list command outputs status information about all the VMs.

    # pairvm list

An individual VM can be started or stopped:

    # pairvm start myvm

    # pairvm stop myvm

VMs will also stop if the guest operating system halts or reboots.

Access to the VM's console is via VNC and the ports are only bound
locally. The VNC display numbers for VMs are displayed by `pairvm list`.
It is also possible to access a VM's virtual serial port:

    # pairvm serial myvm

### Backups

PairVM has a mechanism for backing up VMs. The backup usually happens on
the host which is not running the VM so that backups to not cause
performance issues. A snapshot of the disc is taken and compressed with
`gzip` before being sent via SSH to the backup host.

    # pairvm backup myvm user@backuphost:/backup/myvm.gz 1024

In this example the VM `myvm` is backed up to the `/backup/myvm.gz` on
`backuphost` (SSHing as user `user`). The backup is sent at a speed of
no more than 1MiB/s.

Any occurrence of `_NAME` in the destination will be substituted for the
VM's name. Specifying a VM of "all" will back up each VM in turn.
