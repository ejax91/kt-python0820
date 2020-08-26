import textfsm
from netmiko import ConnectHandler    
from datetime import datetime
import sys                                                                                                 

def get_command(device_info, command_list):
	cmd_output = ""
	device = {
		'device_type': 'cisco_ios',
		'host': device_info["ip_addr"],
		'username': device_info["username"],
		'password': device_info["password"]
	}

	dev_connect = ConnectHandler(**device) 

	for command in command_list:
		cmd_output += dev_connect.send_command(command)

	return cmd_output

# end point ip address
ep_address = "10.1.1.101"

gateway_list = [
	{
		"ip_addr": "10.1.1.101",
		"username": "bca",
		"password": "Janganmasuk321" 
	},
	{
		"ip_addr": "10.1.1.102",
		"username": "bca",
		"password": "Janganmasuk321" 
	}
]

# get mac address from ip address
command_list = ["term len 0", "show ip arp"]

found = False
gw_address = ""
dev_address = ""
for device in gateway_list:
	print("Retrieving MAC addresses for gateway device {}".format(device["ip_addr"]))
	cli_output = get_command(device, command_list)

	with open("show_ip_arp.template") as f:
		template = textfsm.TextFSM(f)
	fsm_results = template.ParseText(cli_output)

	for row in fsm_results:
		if row[0] == ep_address:
			found = True
			gw_address = device["ip_addr"]
			dev_address = row[1]

if found:
	print("Endpoint is found in gateway device {} with MAC: {}".format(gw_address, dev_address))

	switch_list = [
		{
			"ip_addr": "10.1.1.101",
			"username": "bca",
			"password": "Janganmasuk321" 
		},
		{
			"ip_addr": "10.1.1.102",
			"username": "bca",
			"password": "Janganmasuk321" 
		}
	]

	# get mac address from ip address
	command_list = ["term len 0", "show mac address-table"]

	found = False
	sw_address = ""
	vlan_num = ""
	interface_number = ""
	for device in switch_list:
		print("Retrieving interface data for switch device {}".format(device["ip_addr"]))
		cli_output = get_command(device, command_list)

		with open("show_mac_address.template") as f:
			template = textfsm.TextFSM(f)
		fsm_results = template.ParseText(cli_output)

		# TBD: define 'show mac address-table' parsing template
		# TBD: print out the output in formatted mode

		for row in fsm_results:
			if row[0] == ep_address:
				found = True
				sw_address = device["ip_addr"]
				dev_address = row[1]