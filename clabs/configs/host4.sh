#!/bin/bash
# Update the package list and upgrade existing packages
sudo apt update -y && sudo apt upgrade -y

# Install vlan
sudo apt install -y vlan

# Install iproute2
sudo apt install -y iproute2

# Install ping
sudo apt install -y iputils-ping

# Install net-tools so arp command works
sudo apt install -y net-tools

# Install tcpdump
sudo apt install -y tcpdump

# Creating a bonded Ethernet interface (bond0)
sudo ip link add bond0 type bond mode 802.3ad
sudo ip link set eth1 down
sudo ip link set eth1 master bond0
sudo ip link set eth2 down
sudo ip link set eth2 master bond0
sudo ip link set eth3 down
sudo ip link set eth3 master bond0
sudo ip link set eth4 down
sudo ip link set eth4 master bond0
sudo ip link set bond0 up
sudo ip link add link bond0 name bond0.78 type vlan id 78
sudo ip link set bond0.78 up
sudo ip addr add 10.78.78.78/24 dev bond0.78