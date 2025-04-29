#!/bin/bash
# Update the package list and upgrade existing packages
apt update -y && apt upgrade -y

# Install new packages
apt install -y vlan iproute2 iputils-ping net-tools tcpdump iperf3

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
ip link add link bond0 name bond0.34 type vlan id 34
ip link set bond0.34 up
ip addr add 10.34.34.34/24 dev bond0.34
ip route add 10.78.78.0/24 via 10.34.34.1

#Start iperf server and run the client to my peer
# iperf3 -s &
# iperf3 -c 10.78.78.78