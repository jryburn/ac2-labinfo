#!/bin/bash
# Update the package list and upgrade existing packages
apt update -y && apt upgrade -y

# Install vlan
apt install -y vlan

# Install iproute2
apt install -y iproute2

# Install ping
apt install -y iputils-ping

# Install net-tools so arp command works
apt install -y net-tools

# Install tcpdump
apt install -y tcpdump

# Creating a bonded Ethernet interface (bond0)
ip link add bond0 type bond mode 802.3ad
ip link set eth1 down
ip link set eth1 master bond0
ip link set eth2 down
ip link set eth2 master bond0
ip link set eth3 down
ip link set eth3 master bond0
ip link set eth4 down
ip link set eth4 master bond0
ip link set bond0 up
ip link add link bond0 name bond0.40 type vlan id 40
ip link set bond0.40 up
ip addr add 10.40.40.10/24 dev bond0.40