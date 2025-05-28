Network MAC Tracker
This script automates the process of searching for multiple MAC addresses across a fleet of Cisco switches. It connects to devices via SSH using Netmiko, searches for each MAC address, and retrieves detailed interface information where a match is found.
🔧 Features
Reads a list of devices from devices.txt
Reads multiple MAC address patterns from input.txt
Connects to each device using SSH (Cisco IOS)
Searches MAC addresses using show mac address-table
Extracts the interface if a match is found
Retrieves:
Running configuration of the matched interface
Interface status
Device hostname
Logs all results to output.txt (nothing is printed to the console)
Displays a final acknowledgment when complete
📁 File Structure
Search.py: Main script
devices.txt: List of switch IPs (one per line)
input.txt: List of MAC addresses or search patterns (one per line)
output.txt: All matched results and outputs are saved here
📦 Requirements
Python 3.x
Netmiko
bashCopyEditpip install netmiko
🔐 Security Notes
Password input is securely hidden using getpass
Consider using SSH keys or environment variables for automation in secure environments
✅ Usage
bashCopyEditpython Search.py
You'll be prompted for a password once; then the script will automatically connect to each switch, search for the MAC addresses, and save everything to output.txt.
