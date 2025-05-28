import re
from netmiko import ConnectHandler
import getpass

USERNAME = "jkhunt-a"
PASSWORD = getpass.getpass("Enter password: ")

DEVICE_TYPE = "cisco_ios"
DEVICE_FILE = "devices.txt"
PATTERN_FILE = "input.txt"
OUTPUT_FILE = "output.txt"

with open(DEVICE_FILE, 'r') as f:
    devices = [line.strip() for line in f if line.strip()]

with open(PATTERN_FILE, 'r') as f:
    patterns = [line.strip() for line in f if line.strip()]

with open(OUTPUT_FILE, 'w') as log:
    for ip in devices:
        log.write(f"\nConnecting to {ip}...\n")
        try:
            device = {
                'device_type': DEVICE_TYPE,
                'host': ip,
                'username': USERNAME,
                'password': PASSWORD,
            }
            connection = ConnectHandler(**device)

            # Get hostname
            hostname_output = connection.send_command("show run | include hostname")
            hostname_match = re.search(r"hostname\s+(\S+)", hostname_output)
            hostname = hostname_match.group(1) if hostname_match else "Unknown"

            log.write(f"\nConnected to device with hostname: {hostname}\n")

            for pattern in patterns:
                log.write(f"\n--- Searching for pattern: {pattern} on {hostname} ({ip}) ---\n")

                mac_cmd = f"show mac address-table | include {pattern}"
                output = connection.send_command(mac_cmd)

                if output:
                    log.write(f"\n[Hostname: {hostname}] [MAC: {pattern}] Match found:\n{output}\n")

                    lines = output.splitlines()
                    for line in lines:
                        match = re.search(r"(Gi|GigabitEthernet|Fa|FastEthernet)\S+", line)
                        if match:
                            interface = match.group(0)
                            log.write(f"\n--- Additional Info for Interface: {interface} ---\n")

                            run_cmd = f"show run interface {interface}"
                            status_cmd = f"show interface {interface} status"

                            run_output = connection.send_command(run_cmd)
                            status_output = connection.send_command(status_cmd)

                            log.write(f"\n[Running Config for {interface} on {hostname}]:\n{run_output}\n")
                            log.write(f"\n[Status for {interface} on {hostname}]:\n{status_output}\n")
                else:
                    log.write(f"No match found for {pattern} on {hostname} ({ip}).\n")

            connection.disconnect()
        except Exception as e:
            log.write(f"Failed to connect to {ip}: {e}\n")

print(f"\n✅ All results have been saved to '{OUTPUT_FILE}'")
