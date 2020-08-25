import pymongo
from netmiko import ConnectHandler    
from datetime import datetime                                                                                                     

def push_config(device_info, command_list):
	device = {
		'device_type': 'cisco_ios',
		'host': device_info["ip_addr"],
		'username': device_info["username"],
		'password': device_info["password"]
	}

	dev_connect = ConnectHandler(**device) 

	cmd_output = dev_connect.send_config_set(command_list)

	return cmd_output

client = pymongo.MongoClient()
db = client.fwiratam

command_list = []
with open('commands.txt') as f:
	command_list = f.readlines()
	command_list = [cmd.strip() for cmd in command_list]

for device in db.devices.find():
	cmd_output = push_config(device, command_list)
	db.push_config.insert_one({
		"device_id": str(device["_id"]),
		"timestamp": datetime.utcnow(),
		"cmd_output": cmd_output
		})
	print("Succesfully pushed config to device {}!".format(device["name"]))
