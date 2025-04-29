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
ip link add link bond0 name bond0.40 type vlan id 40
ip link set bond0.40 up
ip addr add 10.40.40.10/24 dev bond0.40

#Start iperf server
cat <<- EOF >   /etc/systemd/system/iperf3.service
[Unit]
Description=iperf3 server

[Service]
ExecStart=/usr/bin/iperf3 -s

[Install]
WantedBy=multi-user.target
EOF

service iperf3 start

# Run the client to my peer
iperf3 -c 10.40.40.30