import turtle
import random

class Device():
    def __init__(self, type, caption):
        self.obj_instance = turtle.Turtle()
        self.type = type
        self.speed = 0
        self.x_cor = random.randint(0, 400)
        self.y_cor = random.randint(0, 250)
        self.caption = caption
        self.no_of_interfaces = 1
        self.set_properties_and_create()
        self.caption_obj_instance = self.create_caption()

    def set_properties_and_create(self):
        self.obj_instance.speed(self.speed)
        if self.type == 'node':
            self.obj_instance.shape('router.gif')
        else:
            self.obj_instance.shape('host.gif')
        self.obj_instance.penup()
        self.obj_instance.setposition(self.x_cor, self.y_cor)
        self.obj_instance.ondrag(self.obj_instance.goto)
        self.obj_instance.onrelease(self.is_position_changed)

    def create_caption(self):
        caption_obj = turtle.Turtle()
        caption_obj.speed(0)
        caption_obj.penup()
        if self.type == 'node':
            caption_obj.goto(self.x_cor-12, self.y_cor-40)
        else: 
            caption_obj.goto(self.x_cor-15, self.y_cor-60)
        caption_obj.pendown()
        caption_obj.write(self.caption)
        caption_obj.hideturtle()
        return caption_obj
    
    def is_position_changed(self, x, y):
        new_x_cor = self.obj_instance.xcor()
        new_y_cor = self.obj_instance.ycor()
        if self.x_cor != new_x_cor or self.y_cor != new_y_cor:
            self.x_cor = int(new_x_cor)
            self.y_cor = int(new_y_cor)
            self.update_caption_location()

    def update_caption_location(self):
        self.caption_obj_instance.clear()
        self.caption_obj_instance.penup()
        if self.type == 'node':
            self.caption_obj_instance.goto(self.x_cor-12, self.y_cor-40)
        else:
            self.caption_obj_instance.goto(self.x_cor-15, self.y_cor-60)
        self.caption_obj_instance.pendown()
        self.caption_obj_instance.write(self.caption)

    def disable_drag(self):
        self.obj_instance.ondrag(lambda x, y: x+y)

    def enable_drag(self):
        self.obj_instance.ondrag(self.obj_instance.goto)

    def edit_name(self, *args, **kwargs):
        new_caption = turtle.textinput(f"Edit Name of {self.caption}", "New Name?")
        if new_caption == '':
            pass
        else:
            self.caption = new_caption
            self.update_caption_location()
    
    def enable_edit_name(self):
        self.obj_instance.onclick(self.edit_name)

    def disable_edit_name(self):
        self.obj_instance.onclick(lambda x, y: x+y)