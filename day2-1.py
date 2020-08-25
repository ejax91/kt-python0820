from datetime import datetime
from elasticsearch import Elasticsearch
import paramiko
import time
import re

def show_interface(hostname):
	my_username = 'bca'
	my_password = 'Janganmasuk321'
	port = 22

	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.WarningPolicy)

	client.connect(hostname, port=port, username=my_username, password=my_password)
	channel = client.invoke_shell()

	out = channel.recv(9999)

	channel.send('term len 0\nshow interfaces\n')
	time.sleep(3)

	out = channel.recv(9999)

	cmd_output = out.decode("ascii")

	client.close()	

	my_interface_list = []
	my_interface = {}
	my_router = {}

	iface_pattern = r"(\S+) is (administratively )*(up|down),"
	input_rate_pattern = r"5 minute input rate (\d+) bits/sec"
	output_rate_pattern = r"5 minute output rate (\d+) bits/sec"
	end_string = "output buffer failures"
	for line in cmd_output.split('\n'):
		iface_match = re.match(iface_pattern, line.strip())
		if iface_match:
			my_interface = {"name": iface_match.group(1)}
		if my_interface:
			input_rate_match = re.match(input_rate_pattern, line.strip())
			if input_rate_match:
				my_interface["input_rate"] = input_rate_match.group(1)

			output_rate_match = re.match(output_rate_pattern, line.strip())
			if output_rate_match:
				my_interface["output_rate"] = output_rate_match.group(1)

			if end_string in line:
				my_interface_list.append(my_interface)
				my_interface = {}

	return my_interface_list

if __name__ == '__main__':
	hostname = '10.1.1.101'
	es_host = 'localhost:9200'
	index_name = 'fwiratam'

	es = Elasticsearch([es_host])

	doc_list = show_interface(hostname)

	for doc in doc_list:
		print(doc)

		doc["timestamp"] = datetime.utcnow()
		res = es.index(index=index_name, body=doc)
		print(res['result'])