import pyeapi
import requests

# Kentik email, token, and API base URL
# Replace with your Kentik account email located at:
# https://portal.kentik.com/v4/profile/general
KENTIK_API_EMAIL = "user@domain.com"
# Replace with your Kentik API token located at:
# https://portal.kentik.com/v4/profile/auth
KENTIK_API_TOKEN = "mylongapitoken"
KENTIK_API_BASE_URL = "https://grpc.api.kentik.com/device/v202308beta1/device"

# Arista device username and password
ARISTA_USERNAME = "admin"
ARISTA_PASSWORD = "admin"

# List of devices to configure
devices = [
    {
        "ip": "172.20.20.11",
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "leaf1",
    },
    {
        "ip": "172.20.20.12",
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "leaf2",
    },
    {
        "ip": "172.20.20.13",
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "leaf3",
    },
    {
        "ip": "172.20.20.14",
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "leaf4",
    },
    {
        "ip": "172.20.20.15",
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "leaf5",
    },
    {
        "ip": "172.20.20.16",
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "leaf6",
    },
    {
        "ip": "172.20.20.17",
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "leaf7",
    },
    {
        "ip": "172.20.20.18",
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "leaf8",
    },
    {
        "ip": "172.20.20.21",
        "username": ARISTA_USERNAME,
        "password": ARISTA_PASSWORD,
        "kentik_device_name": "spine1",
    },
    {
        "ip": "172.20.20.22",
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


# Function to configure sFlow on the Arista switch using PYEAPI
def configure_sflow_on_switch(device):
    try:
        # Connect to the Arista switch
        node = pyeapi.connect(
            transport="https",
            host=device["ip"],
            username=device["username"],
            password=device["password"],
            return_node=True,
            port=443
        )

        # sFlow configuration commands
        sflow_commands = [
            'enable',
            'configure terminal',
            'sflow run',
            'sflow destination 172.20.20.1 9995',
            'sflow source-interface Management0',
            'sflow sample 512',
            'sflow polling-interval 30',
        ]

        # Execute the commands on the Arista switch
        node.config(sflow_commands)
        print(f"sFlow configuration applied to switch  {device['ip']}.")
    except Exception as e:
        print(f"Failed to configure sFlow on the switch {device['ip']}: {e}")


# Main function to loop through each device, configure sFlow,
# and then send batch update to Kentik
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
