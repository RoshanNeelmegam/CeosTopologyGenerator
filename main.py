import turtle
from button import Button
from device import Device
from connection import Connection
from topology_yaml import Topology_yaml
from device_board import DeviceBoard

# global variables
switch_count = 1
host_count =1 
devices_dict = {'nodes': {}, 'hosts': {}}
is_link_mode_on = False
is_edit_mode_on = False
connections_list = []
is_connection_in_progress = False
starting_points = ()
starting_device = None
topology_info = None
switch_image = ''
host_image = ''

topo_screen = turtle.Screen()
topo_screen.setup(1500, 900)
topo_screen.bgcolor("ghost white")
topo_screen.register_shape('router.gif')
topo_screen.register_shape('host.gif')
board = DeviceBoard()

def add_nodes_func(*args, **kwargs):
    global switch_count
    global devices_dict
    number_of_nodes = int(turtle.textinput('Switches Prompt?', "No of Switches/Routers?"))
    for node_no in range(switch_count, number_of_nodes+switch_count):
        node = Device('node', f'Switch{node_no}')
        # devices_dict['nodes'][node] = {'name': f'Switch{node_no}', 'no_of_interfaces': 1}
        devices_dict['nodes'][node] = {}
    switch_count += number_of_nodes

def add_hosts_func(*args, **kwargs):
    global host_count
    number_of_hosts = int(turtle.textinput('Hosts Prompt?', "No of Hosts?"))
    for host_no in range(host_count, number_of_hosts+host_count):
        host = Device('host', f'Host{host_no}')
        # devices_dict['hosts'][host] = {'name': f'Host{host_no}', 'no_of_interfaces': 1}
        devices_dict['hosts'][host] = {}
    host_count += number_of_hosts

def create_connections(x, y):
    global is_connection_in_progress
    global devices_dict
    global starting_points
    global starting_device
    global board
    if not is_connection_in_progress:
        starting_points = (x, y)
        starting_device = None
        for top_device in devices_dict:
            for device in devices_dict[top_device]:
                if device.obj_instance.distance(starting_points) < 40:
                    starting_device = device
        if starting_device is None:
            # print('yes new instance of link mode')
            return
        is_connection_in_progress = True
        board.display(starting_device=starting_device.caption)
    else:   
        ending_points = (x, y)
        ending_device = None
        for top_device in devices_dict:
            for device in devices_dict[top_device]:
                if device.obj_instance.distance(ending_points) < 40:
                    ending_device = device
        if starting_device == ending_device:
            board.display()
            is_connection_in_progress = False
            return
        elif ending_device is None:
            # print('no proper end so continuing instance from next')
            board.display(starting_device=starting_device.caption)
            return
        else:
            # print('new or old instance for ending')
            board.display(starting_device=starting_device.caption, ending_device=ending_device.caption)
            connection = Connection(starting_points, ending_points)
            connection.create()
            connections_list.append(f'"{starting_device.caption}:eth{starting_device.no_of_interfaces}", "{ending_device.caption}:eth{ending_device.no_of_interfaces}"')
            starting_device.no_of_interfaces += 1
            ending_device.no_of_interfaces += 1
            is_connection_in_progress = False
         
def toggle_link_mode(*args, **kwargs):
    global is_link_mode_on
    link_mode.flicker_button('darkolivegreen4')
    if not is_link_mode_on:
        is_link_mode_on = True
        for top_device in devices_dict:
            for device in devices_dict[top_device]:
                device.disable_drag()
        topo_screen.onclick(create_connections)
    else:
        is_link_mode_on = False
        for top_device in devices_dict:
            for device in devices_dict[top_device]:
                device.enable_drag()
        topo_screen.onclick(lambda x, y: (x, y))

def toggle_edit_mode(*args, **kwargs):   
    global is_edit_mode_on
    edit_device.flicker_button('coral3')
    if not is_edit_mode_on:
        is_edit_mode_on = True
        for top_device in devices_dict:
            for device in devices_dict[top_device]:
                device.disable_drag()
                device.enable_edit_name()
    else:
        is_edit_mode_on = False
        for top_device in devices_dict:
            for device in devices_dict[top_device]:
                device.enable_drag()
                device.disable_edit_name()

def submit_yaml(*args, **kwargs):
    global devices_dict
    global connections_list
    global topology_info
    switch_image = "ceosimage:4.32.2F"
    # host_image="alpine-host"
    host_image = "ceosimage:4.32.2F"
    switch_kind = "ceos"
    # host_kind="host"
    host_kind = "host"
    mgmt_ip="172.200.200.0/24"
    if topology_info is None: 
        topology_info = Topology_yaml(devices_dict, connections_list, switch_image, host_image, switch_kind, host_kind, mgmt_ip)
    print(topology_info.create_yaml(device_dict=devices_dict, connections_list=connections_list))

# creating buttons
add_nodes = Button(-660, 400, 'crimson', add_nodes_func, 'Add Nodes')
add_hosts = Button(-570, 400, 'dodgerblue2', add_hosts_func, 'Add Hosts')
link_mode = Button(-480, 400, 'darkolivegreen1', toggle_link_mode, 'Link Mode')
edit_device = Button(-390, 400, 'coral' , toggle_edit_mode, 'Edit device')
submit = Button(-300, 400, 'bisque' , submit_yaml, 'Submit')








































topo_screen.mainloop()