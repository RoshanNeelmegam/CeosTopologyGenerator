import random
import re

awesome_names = ['Hendrix','Cayson','Petronilla','Phaidra','Osbert','Logen','Gelina','Eraqus','Olivero','Fosca','Serkr','Martti','MJ','Ihrin','Puleleiite','Rizalino','Vixen','Bower','Fonsie']

class Topology_yaml():
    def __init__(self, device_dict, connections_list, switch_image, host_image, switch_kind, host_kind, mgmt_ip):
        self.devices_dict = device_dict
        self.connection_list = connections_list
        self.switch_image = switch_image
        self.host_image = host_image
        self.mgmt_ip = mgmt_ip
        self.mgmt_subnet = re.findall(r'(\d+\.\d+\.\d+)\.\d+.+', self.mgmt_ip)[0]
        self.ip = 1
        self.switch_kind = switch_kind
        self.host_kind = host_kind
        self.lab_name = f'{random.choice(awesome_names)}{random.randint(0, 1000)}'
        self.contents = ''

    def create_yaml(self, device_dict, connections_list, switch_image=None, host_image=None, switch_kind=None, host_kind=None, mgmt_ip=None):
        if (switch_image is not None or host_image is not None or switch_kind is not None or host_kind is not None or mgmt_ip is not None):
            self.switch_image = switch_image
            self.host_image = host_image
            self.mgmt_ip = mgmt_ip
            self.mgmt_subnet = re.findall(r'(\d+\.\d+\.\d+)\.\d+.+')[0]
            self.ip = 10
            self.switch_kind = switch_kind
        self.devices_dict = device_dict
        self.connection_list = connections_list
        self.contents = ''
        self.contents = f"""
name: {self.lab_name}
topology:
  kinds:
    {self.switch_kind}:
      image: {self.switch_image}
    {self.host_kind}:
      image: {self.host_image}
  nodes:"""
        for top_level_device in self.devices_dict:
            if top_level_device == 'nodes':
                for switch in self.devices_dict[top_level_device]:
                    self.contents += f"""
    {switch.caption}:
        kind: {self.switch_kind}
        mgmt-ipv4: {self.mgmt_subnet}.{self.ip}"""
                    self.ip += 1
            elif top_level_device == 'hosts':
                for host in self.devices_dict[top_level_device]:
                    self.contents += f"""
    {host.caption}:
        kind: {self.host_kind}
        mgmt-ipv4: {self.mgmt_subnet}.{self.ip}"""
                    self.ip += 1
        self.contents += """  
  links:"""
        for connections in self.connection_list:
            self.contents += f"""
    - endpoints: [{connections}]"""
        self.contents += f"""
mgmt:
  network: lab_{self.lab_name}_network
  ipv4-subnet: {self.mgmt_ip}"""
        return(self.contents)




