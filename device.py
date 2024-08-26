import turtle

class Node(turtle.Turtle): 
    def __init__(self, link_mode_var, included_dict):
        super().__init__()
        self.global_link_mode_state = link_mode_var
        self.included_dict = included_dict

    def update_caption_pos(self, x, y):
        if self.global_link_mode_state is False:
            print(self.global_link_mode_state)
            try:
                caption_obj = self.included_dict[self]['caption']
            except Exception as e:
                print('Exception occurred while getting caption object')      
            caption_obj.clear()
            caption_obj.penup()
            if self.included_dict[self]['identity'] == 'node':
                caption_obj.goto(x-11, y-40)
            elif self.included_dict[self]['identity'] == 'host':               
                caption_obj.goto(x-15, y-60)
            else:
                print('No other device than host or node is present')
            caption_obj.pendown()
            name = self.included_dict[self]['name']
            caption_obj.write(name)