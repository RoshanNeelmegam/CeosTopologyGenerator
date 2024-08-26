import turtle
import random
import random
import re
from device import Node
from deviceboard import Deviceboard

# setting up the screen and registering shapes
screen = turtle.Screen()
screen.setup(1500, 900)
# registering shapes that could be used while turtle instantiation
screen.register_shape('router.gif')
screen.register_shape('host.gif')
deviceboard = Deviceboard()

# defining variables
number_of_nodes = 0
number_of_hosts = 0
nodes_dict = {} # stores node info in the format {'<turtle_object': {'name': <node>, 'caption': <caption_turtle_object>, 'number_of_interfaces': x}}
hosts_dict = {} # stores node info in the format {'<turtle_object': {'name': <node>, 'caption': <caption_turtle_object>, 'number_of_interfaces': x}}
connections_list = [] # stores connection stats in the format [{'node1': 'eth1', 'node2': 'eth2'}]
global_node_count = 1 # keeps track of numver of nodes/routers
global_host_count = 1 # keeps track of number of hosts

set_nodes = set() 

# variables to keep track of devices during link mode
link_mode_var = False
start_node = None
in_process = False # This is true if first_device is selected during link mode. This will prevent certain click features on the other node until this becomes false again
first_device = ''
second_device = ''

def create_nodes(number_of_nodes):
    global global_node_count
    global link_mode_var
    global nodes_dict
    global hosts_dict
    for i in range(global_node_count, global_node_count+number_of_nodes):
        node_turtle = Node(link_mode_var=link_mode_var, included_dict=nodes_dict)
        node_turtle.speed(0)
        node_turtle.shape('router.gif')
        node_turtle.penup()
        position = (10+random.randint(0, 100),20+random.randint(0, 200))
        node_turtle.setposition(position)
        node_turtle_caption = create_button_or_caption_name(position[0]-11, position[1]-40, f'Node{i}')
        node_turtle.ondrag(node_turtle.goto)
        node_turtle.onrelease(node_turtle.update_caption_pos)
        nodes_dict[node_turtle] = {'name': f'Node{i}', 'caption': node_turtle_caption, 'number_of_interfaces': 1, 'identity': 'node'}
        set_nodes.add(f'node{i}')
    global_node_count += number_of_nodes

def add_nodes(*args, **kwargs):
    number_of_nodes = int(turtle.textinput('Nodes Prompt?', "No of Nodes?"))
    create_nodes(number_of_nodes)
    
def create_hosts(number_of_hosts):
    global global_host_count
    for i in range(global_host_count, global_host_count+number_of_hosts):
        host_turtle = Node(link_mode_var, included_dict=hosts_dict)
        host_turtle.speed(0)
        host_turtle.fillcolor('yellow')
        host_turtle.shape('host.gif')
        host_turtle.penup()
        position = (10+random.randint(0, 100),20+random.randint(0, 200))
        host_turtle.setposition(position)
        host_turtle_caption = create_button_or_caption_name(position[0]-15, position[1]-60, f'Host{i}')
        host_turtle.ondrag(host_turtle.goto)
        host_turtle.onrelease(host_turtle.update_caption_pos)
        hosts_dict[host_turtle] = {'name': f'Host{i}', 'caption': host_turtle_caption, 'number_of_interfaces': 1, 'identity': 'host'}
        set_nodes.add(f'host{i}')
    global_host_count += number_of_hosts
        
def add_hosts(*args, **kwargs):
    number_of_hosts = int(turtle.textinput('Hosts Prompt?', "No of Hosts?"))
    create_hosts(number_of_hosts)

# this function helps in disabling the dragging when link mode is activated
def disable_shit(*args, **kwargs):
    pass

def on_node_click_for_link_mode(x, y):
    global in_process
    global start_node
    global first_device
    global second_device
    if in_process == False and start_node is None: 
        start_node = (x, y)
        in_process = True
    elif in_process == True and start_node is not None:
        end_node = (x, y)
        start_eth = 0
        end_eth = 0

        # Find the start node
        for node_key in nodes_dict:           
            if node_key.distance(start_node) < 45:
                first_device = nodes_dict[node_key]['name']
                print(f'first node is {first_device}')
                start_eth = nodes_dict[node_key]['number_of_interfaces']
                # nodes_dict[node_key]['number_of_interfaces'] += 1
                break
        for host_key in hosts_dict:
            if host_key.distance(start_node) < 45:
                first_device = hosts_dict[host_key]['name']
                print(f'first node is {first_device}')
                start_eth = hosts_dict[host_key]['number_of_interfaces']
                # hosts_dict[host_key]['number_of_interfaces'] += 1
                break
        # Find the end node
        for node_key in nodes_dict:
            if node_key.distance(end_node) < 45:
                second_device = nodes_dict[node_key]['name']
                print(f'second node is {second_device}')
                end_eth = nodes_dict[node_key]['number_of_interfaces']
                # nodes_dict[node_key]['number_of_interfaces'] += 1    
                break    
        for host_key in hosts_dict:
            if host_key.distance(end_node) < 45:
                second_device = hosts_dict[host_key]['name']
                print(f'second node is {second_device}')
                end_eth = hosts_dict[host_key]['number_of_interfaces']
                # hosts_dict[host_key]['number_of_interfaces'] += 1    
                break    
        if first_device != second_device and (first_device != '' and second_device != ''):        
            draw_line(start_node, end_node)
            for nodes in nodes_dict:
                if first_device == nodes_dict[nodes]['name']:
                    nodes_dict[nodes]['number_of_interfaces'] += 1
                elif second_device == nodes_dict[nodes]['name']:
                    nodes_dict[nodes]['number_of_interfaces'] += 1
            for hosts in hosts_dict:
                if first_device == hosts_dict[hosts]['name']:
                    hosts_dict[hosts]['number_of_interfaces'] += 1
                elif second_device == hosts_dict[hosts]['name']:
                    hosts_dict[hosts]['number_of_interfaces'] += 1
            connections_list.append({first_device:f'eth{start_eth}', second_device:f'eth{end_eth}'})    
            deviceboard.updateBoard(connections_list[-1])
            print(connections_list)
        start_node = None
        in_process = False
        first_device = ''
        second_device = ''

def link_mode_nodes_hosts_behaviour(dictionary, link_mode, ondrag_method=disable_shit, onclick_method=on_node_click_for_link_mode):
    if link_mode:
        for device in dictionary:
            device.ondrag(ondrag_method)
            device.onclick(onclick_method)
            device.onrelease(disable_shit)
    else:
         for device in dictionary:
            device.ondrag(device.goto)
            device.onclick(disable_shit)    
            device.onrelease(device.update_caption_pos)   

# link mode disables dragging and enables link addition method
def link_mode(*args, **kwargs):
    global link_mode_var
    if link_mode_var is False:
        update_link_mode_button_and_name('orange', -505, 390)
        link_mode_var = True
        link_mode_nodes_hosts_behaviour(dictionary=nodes_dict, link_mode=link_mode_var)
        link_mode_nodes_hosts_behaviour(dictionary=hosts_dict, link_mode=link_mode_var)   
    else: 
        update_link_mode_button_and_name('green', -505, 390)
        link_mode_var = False
        link_mode_nodes_hosts_behaviour(dictionary=nodes_dict, link_mode=link_mode_var)
        link_mode_nodes_hosts_behaviour(dictionary=hosts_dict, link_mode=link_mode_var)   

# function to draw a line between two points
def draw_line(start, end):
    line = turtle.Turtle()
    line.speed(0)
    line.hideturtle()
    line.penup()
    line.goto(start)
    line.pendown()
    line.goto(end)
    line.penup()
    line.hideturtle()

def create_button(x_cor, y_cor, color, on_click_method):
    button_obj = turtle.Turtle()
    button_obj.speed(0)
    button_obj.shape('square')
    button_obj.color(color)
    button_obj.penup()
    button_obj.goto(x_cor, y_cor)
    button_obj.shapesize(2,4)
    button_obj.onclick(on_click_method)    
    return button_obj

def create_button_or_caption_name(x_cor, y_cor, caption):
    button_name_obj = turtle.Turtle()
    button_name_obj.speed(0)
    button_name_obj.penup()
    button_name_obj.goto(x_cor, y_cor)
    button_name_obj.pendown()
    button_name_obj.write(caption)
    button_name_obj.hideturtle()
    return button_name_obj

def update_link_mode_button_and_name(color, x_cor, y_cor):
    link_mode_button.color(color)
    link_mode_button_text.goto(x_cor, y_cor)
    link_mode_button_text.pendown()
    link_mode_button_text.write('Link Mode')
    
def submit_to_file(node_image = "ceosimage:4.27.3F", host_image = "alpine-host", mgmt_ip = '172.100.100.0/24'):
    ip = 10 # indicates the ip of the device in that subnet
    subnet = re.findall(r'(\d+\.\d+\.\d+)\.\d+.+', mgmt_ip)[0] # gets the network part
    contents = f"""
name: Lab{random.randint(0, 1000)}
topology:
  kinds:
    ceos:
      image: {node_image}
    host:
      image: {host_image}
  nodes:"""
    for device in nodes_dict:
        contents += f"""
    {nodes_dict[device]['name']}:
        kind: ceos
        mgmt-ipv4: {subnet}.{ip}"""
        ip += 1
    for device in hosts_dict:
        contents += f"""
    {hosts_dict[device]['name']}:
        kind: host
        mgmt-ipv4: {subnet}.{ip}"""
        ip += 1
    contents += """  
    links:"""
    temp_list = []
    for conn in connections_list:
        endpoints = ''
        for device, ethernet in conn.items():
            endpoints += f"\"{device}\":\"{ethernet}\", "
        endpoints = endpoints.removesuffix(', ')
        temp_list.append(endpoints)
    
    for conn in temp_list:
        contents += f"""
      - endpoints: [{conn}]"""
    
    contents += f"""
mgmt:
  network: LabNet{random.randint(0,1000)}
  ipv4-subnet: {mgmt_ip}"""
    print(contents)

add_nodes_button = create_button(-660, 400, 'red', add_nodes)
add_nodes_button_text = create_button_or_caption_name(-685, 390, 'Add Nodes')

add_hosts_button = create_button(-570, 400, 'blue', add_hosts)
add_hosts_button_text = create_button_or_caption_name(-595, 390, 'Add Hosts')

link_mode_button = create_button(-480, 400, 'green', link_mode)
link_mode_button_text = create_button_or_caption_name(-505, 390, 'Link Mode')

submit_button = create_button(-390, 400, 'orange' , submit_to_file)
submit_button_text = create_button_or_caption_name(-410, 390, 'Submit')

screen.mainloop()