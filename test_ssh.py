import paramiko
import time
import re

hostname = '10.1.1.101'
my_username = 'bca'
my_password = 'Janganmasuk321'
port = 22

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.WarningPolicy)

client.connect(hostname, port=port, username=my_username, password=my_password)
channel = client.invoke_shell()

out = channel.recv(9999)

channel.send('term len 0\nshow run\n')
time.sleep(3)

out = channel.recv(9999)

show_run = out.decode("ascii")

client.close()

my_interface_list = []
my_interface = {}
my_router = {}

iface_pattern = r"interface (.*)"
ip_addr_pattern = r"ip address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)"
shutdown_pattern = r"shutdown"
end_pattern = r"!"
for line in show_run.split('\n'):
	iface_match = re.match(iface_pattern, line.strip())
	if iface_match:
		my_interface = {"name": iface_match.group(1), "status": "up"}
	if my_interface:
		ip_addr_match = re.match(ip_addr_pattern, line.strip())
		if ip_addr_match:
			my_interface["ip_addr"] = ip_addr_match.group(1)
			my_interface["netmask"] = ip_addr_match.group(2)

		shutdown_match = re.match(shutdown_pattern, line.strip())
		if shutdown_match:
			my_interface["status"] = "down"

		end_match = re.match(end_pattern, line.strip())
		if end_match:
			my_interface_list.append(my_interface)
			my_interface = {}

my_router["interfaces"] = my_interface_list
print(my_router)
