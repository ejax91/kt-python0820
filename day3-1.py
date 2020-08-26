import textfsm
from netmiko import ConnectHandler    
from datetime import datetime                                                                                                     

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

device = {
	"ip_addr": "10.1.1.101",
	"username": "bca",
	"password": "Janganmasuk321" 
}

command_list = ["term len 0", "show ip interface brief"]

cli_output = get_command(device, command_list)

with open("show_iface.template") as f:
	template = textfsm.TextFSM(f)
fsm_results = template.ParseText(cli_output)

for row in fsm_results:
	print(row)