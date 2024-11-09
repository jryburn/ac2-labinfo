# The gNMI portion of this script is not functioning. Do NOT use for now
# without fixing that section.

from pygnmi.client import gNMIclient
import requests

# Kentik email, token, and API base URL
# Replace with your Kentik account email located at:
# https://portal.kentik.com/v4/profile/general
KENTIK_API_EMAIL = "user@domain.com"
# Replace with your Kentik API token located at:
#  https://portal.kentik.com/v4/profile/auth
KENTIK_API_TOKEN = "mylongapikey"
KENTIK_API_BASE_URL = "https://grpc.api.kentik.com/device/v202308beta1/device"

# Arista device username and password
ARISTA_USERNAME = "admin"
ARISTA_PASSWORD = "admin"

# gNMI path for sFlow configuration based on OpenConfig sampling model
SFLOW_PATH = "/sampling/sflow/config"

# List of devices to configure
devices = [
    {
        "ip": "172.20.20.11",
        "port": 57400,  # Default gNMI port, adjust if needed
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "leaf1",
    },
    {
        "ip": "172.20.20.12",
        "port": 57400,  # Default gNMI port, adjust if needed
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "leaf2",
    },
    {
        "ip": "172.20.20.13",
        "port": 57400,  # Default gNMI port, adjust if needed
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "leaf3",
    },
    {
        "ip": "172.20.20.14",
        "port": 57400,  # Default gNMI port, adjust if needed
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "leaf4",
    },
    {
        "ip": "172.20.20.15",
        "port": 57400,  # Default gNMI port, adjust if needed
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "leaf5",
    },
    {
        "ip": "172.20.20.16",
        "port": 57400,  # Default gNMI port, adjust if needed
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "leaf6",
    },
    {
        "ip": "172.20.20.17",
        "port": 57400,  # Default gNMI port, adjust if needed
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "leaf7",
    },
    {
        "ip": "172.20.20.18",
        "port": 57400,  # Default gNMI port, adjust if needed
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "leaf8",
    },
    {
        "ip": "172.20.20.21",
        "port": 57400,  # Default gNMI port, adjust if needed
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "spine1",
    },
    {
        "ip": "172.20.20.22",
        "port": 57400,  # Default gNMI port, adjust if needed
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "spine2",
    },
    # Add more devices as needed
]


# Function to get device_id from Kentik by device name
def get_device_id_from_kentik(device_name):
    headers = {
        'X-CH-Auth-Email': f"{KENTIK_API_EMAIL}",
        'X-CH-Auth-API-Token': f"{KENTIK_API_TOKEN}",
        'Content-Type': 'application/json',
    }

    # Retrieve the list of devices from Kentik
    try:
        response = requests.get(KENTIK_API_BASE_URL, headers=headers, timeout=10)
        response.raise_for_status()
        devices_list = response.json().get("devices", [])

        # Find the device ID for the given device name
        for device in devices_list:
            if device.get("deviceName") == device_name:
                return device.get("id")
        print(f"Device '{device_name}' not found in Kentik.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve devices from Kentik: {e}")

    return None


# Function to send batch update to Kentik
def configure_device_in_kentik(device):
    # Retrieve the device_id if not already available
    if not device.get("device_id"):
        device_id = get_device_id_from_kentik(device["kentik_device_name"])
        if not device_id:
            print(f"Skipping Kentik configuration for {device['kentik_device_name']} due to missing device_id.")
            return
        device["device_id"] = device_id

    headers = {
        'X-CH-Auth-Email': f"{KENTIK_API_EMAIL}",
        'X-CH-Auth-API-Token': f"{KENTIK_API_TOKEN}",
        'Content-Type': 'application/json',
    }

    # Kentik device payload for configuration
    payload = {
        "device": {
            "id": device["device_id"],
            "deviceName": device["kentik_device_name"],
            "sendingIps": [device["ip"]],
            "planId": 12345,  # Replace with your Kentik plan ID
            "siteId": 12345,  # Replace with your Kentik site ID
            "deviceSampleRate": 512,
            "deviceDescription": f"{device['kentik_device_name']} configured for sFlow"
        }
    }

    # Send device update request to Kentik
    url = f"{KENTIK_API_BASE_URL}/{device['device_id']}"
    try:
        response = requests.put(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        print(f"Device {device['kentik_device_name']} updated in Kentik:")
    except requests.exceptions.RequestException as e:
        print(f"Failed to update device {device['kentik_device_name']} in Kentik: {e}")


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


def main():
    # Step 1: Update devices in Kentik with the IPs that will sending flow
    for device in devices:
        configure_device_in_kentik(device)

    # Step 2: Configure sFlow on each switch
    for device in devices:
        print(f"Configuring device: {device['kentik_device_name']} ({device['ip']})")
        configure_sflow_on_switch(device)


if __name__ == "__main__":
    main()
