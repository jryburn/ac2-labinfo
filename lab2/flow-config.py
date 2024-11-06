import pyeapi
import requests

# Kentik API token and base URL
KENTIK_API_TOKEN = "YOUR_KENTIK_API_TOKEN"
KENTIK_API_BASE_URL = "https://api.kentik.com/api/v202308beta1/device"

# List of devices to configure
devices = [
    {
        "ip": "SWITCH_IP_1",
        "username": "USERNAME_1",
        "password": "PASSWORD_1",
        "kentik_device_name": "Arista Switch 1",
        "sending_ip": "10.10.10.1",  # sFlow sending IP
    },
    {
        "ip": "SWITCH_IP_2",
        "username": "USERNAME_2",
        "password": "PASSWORD_2",
        "kentik_device_name": "Arista Switch 2",
        "sending_ip": "10.10.10.2",  # sFlow sending IP
    },
    # Add more devices as needed
]

# Function to configure sFlow on the Arista switch using PYEAPI
def configure_sflow_on_switch(ip, username, password, sending_ip):
    try:
        # Connect to the Arista switch
        node = pyeapi.connect(
            transport="https",
            host=ip,
            username=username,
            password=password,
            return_node=True,
            port=443
        )

        # sFlow configuration commands
        sflow_commands = [
            'enable',
            'configure terminal',
            'sflow',
            f'sflow collector 10.10.10.10',  # Replace with your sFlow collector IP
            f'sflow agent ip {sending_ip}',
            'sflow sample 512',
            'sflow polling-interval 30',
        ]

        # Execute the commands on the Arista switch
        node.config(sflow_commands)
        print(f"sFlow configuration applied to switch {ip}.")
    except Exception as e:
        print(f"Failed to configure sFlow on the switch {ip}: {e}")

# Function to configure the device in Kentik
def configure_device_in_kentik(kentik_device_name, sending_ip):
    headers = {
        'Authorization': f"Bearer {KENTIK_API_TOKEN}",
        'Content-Type': 'application/json',
    }

    # Kentik device payload for configuration
    payload = {
        "device": {
            "device_name": kentik_device_name,
            "device_type": "router",
            "sending_ips": [sending_ip],
            "plan_id": 12345,  # Replace with your Kentik plan ID
            "device_sample_rate": 512,
            "description": f"{kentik_device_name} configured for sFlow",
        }
    }

    # Send request to Kentik API to add the device
    try:
        response = requests.post(
            KENTIK_API_BASE_URL, headers=headers, json=payload
        )
        response.raise_for_status()
        print(f"Device {kentik_device_name} configured in Kentik:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Failed to configure device {kentik_device_name} in Kentik: {e}")

# Main function to loop through each device and configure sFlow and Kentik
def main():
    for device in devices:
        print(f"Configuring device: {device['kentik_device_name']} ({device['ip']})")

        # Step 1: Configure sFlow on the switch
        configure_sflow_on_switch(
            device["ip"],
            device["username"],
            device["password"],
            device["sending_ip"]
        )
        
        # Step 2: Configure device in Kentik
        configure_device_in_kentik(
            device["kentik_device_name"],
            device["sending_ip"]
        )

if __name__ == "__main__":
    main()
