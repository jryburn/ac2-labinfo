import json
from pygnmi.client import gNMIclient
import requests

# Kentik email, token, and API base URL
KENTIK_API_EMAIL = "justin@ryburn.org" # Replace with your Kentik account email
KENTIK_API_TOKEN = "fdd6e813e675f3e3431d616a7039e1e9" # Replace with your Kentik API token
KENTIK_API_BASE_URL = "https://api.kentik.com/api/v202308beta1/device/batch"

# Arista device username and password
ARISTA_USERNAME = "admin"
ARISTA_PASSWORD = "admin"


# List of devices to configure
devices = [
    {
        "ip": "172.20.20.5",
        "port": 57400, # Default gNMI port, adjust if needed
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "leaf1",
    },
    {
        "ip": "172.20.20.9",
        "port": 57400, # Default gNMI port, adjust if needed
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "leaf2",
    },
    {
        "ip": "172.20.20.15",
        "port": 57400, # Default gNMI port, adjust if needed
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "leaf3",
    },
    {
        "ip": "172.20.20.12",
        "port": 57400, # Default gNMI port, adjust if needed
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "leaf4",
    },
    {
        "ip": "172.20.20.8",
        "port": 57400, # Default gNMI port, adjust if needed
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "leaf5",
    },
    {
        "ip": "172.20.20.4",
        "port": 57400, # Default gNMI port, adjust if needed
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "leaf6",
    },
    {
        "ip": "172.20.20.2",
        "port": 57400, # Default gNMI port, adjust if needed
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "leaf7",
    },
    {
        "ip": "172.20.20.13",
        "port": 57400, # Default gNMI port, adjust if needed
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "leaf8",
    },
    {
        "ip": "172.20.20.6",
        "port": 57400, # Default gNMI port, adjust if needed
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "spine1",
    },
    {
        "ip": "172.20.20.7",
        "port": 57400, # Default gNMI port, adjust if needed
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "spine2",
    },
    # Add more devices as needed
]

# Function to create a batch payload for Kentik device update
### TODO: add the autocon tag to the devices ###
### Also add sites so it shows up on teh map ###
def prepare_kentik_batch_payload(devices):
    batch_payload = []
    for device in devices:
        device_config = {
            "device_name": device["kentik_device_name"],
            "sending_ips": [device["ip"]],
            "planId": 12345,  # Replace with your Kentik plan ID
            "siteId": 12345, # Replace with your Site ID for Autocon2
            "deviceSampleRate": 512,
        }
        batch_payload.append(device_config)
    return {"devices": batch_payload}

# Function to send batch update to Kentik
def configure_devices_in_kentik_batch(devices):
    headers = {
        'X-CH-Auth-API-Token': f"Bearer {KENTIK_API_EMAIL}",
        'X-CH-Auth-Email': f"Bearer {KENTIK_API_TOKEN}",
        'Content-Type': 'application/json',
    }

    # Prepare the payload for batch update
    payload = prepare_kentik_batch_payload(devices)

    # Send batch update request to Kentik
    try:
        response = requests.put(
            KENTIK_API_BATCH_URL, headers=headers, json=payload
        )
        response.raise_for_status()
        print("Devices configured in Kentik:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Failed to configure devices in Kentik: {e}")

# Function to configure sFlow on the Arista switch using gNMI and OpenConfig
def configure_sflow_on_switch(device):
    sflow_config = {
        "sflow": {
            "config": {
                "agent-id": device["ip"],
                "collector-address": "172.20.20.1",
                "sample-rate": 512,
                "polling-interval": 30
            }
        }
    }

    # Establish gNMI connection to the device
    target = (device["ip"], device["port"])
    try:
        with gNMIclient(target=target, username=device["username"], password=device["password"], insecure=True) as gnmi:
            # Update sFlow configuration
            result = gnmi.set(update=[(SFLOW_PATH, sflow_config)])
            print(f"sFlow configuration applied to switch {device['ip']}:", result)
    except Exception as e:
        print(f"Failed to configure sFlow on the switch {device['ip']}: {e}")

# Main function to loop through each device, configure sFlow, and then send batch update to Kentik
def main():
    # Step 1: Configure all devices in Kentik in a single batch update
    configure_devices_in_kentik_batch(devices)

    # Step 2: Configure sFlow on each switch
    for device in devices:
        print(f"Configuring device: {device['kentik_device_name']} ({device['ip']})")
        configure_sflow_on_switch(device)    

if __name__ == "__main__":
    main()
