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

command_list = ["term len 0", "show run | sec crypto map"]

# cli_output = get_command(device, command_list)

cli_output = """
crypto map VPN-L2L-Network 1 match address ITWorx_domain
crypto map VPN-L2L-Network 1 set pfs	
crypto map VPN-L2L-Network 1 set peer 212.25.140.19
crypto map VPN-L2L-Network 1 set ikev1 transform-set ESP-AES-256-SHA
crypto map VPN-L2L-Network 2 match address outside_cryptomap
crypto map VPN-L2L-Network 2 set peer 21.146.142.47
crypto map VPN-L2L-Network 2 set ikev1 transform-set L2L
crypto map VPN-L2L-Network 3 match address outside_3_cryptomap
crypto map VPN-L2L-Network 3 set peer 12.41.40.96
crypto map VPN-L2L-Network 3 set ikev1 transform-set ESP-AES-128-SHA"""

with open("crypto_map.template") as f:
	template = textfsm.TextFSM(f)
fsm_results = template.ParseText(cli_output)

crypto_map_list = []
for row in fsm_results:
	crypto_map_dict = {
		"address": row[0],
		"name": row[1],
		"sequence": row[2],
		"peer": row[4],
		"ike_version": row[5],
		"transform": row[6]
	}
	crypto_map_list.append(crypto_map_dict)

print(crypto_map_lists)