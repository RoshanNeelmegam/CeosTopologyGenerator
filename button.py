import turtle

class Button():
    def __init__(self, x_cor, y_cor, color, on_click_method, caption):
        self.obj_instance = turtle.Turtle()
        self.shape = 'square'
        self.speed = 0
        self.x_cor = x_cor
        self.y_cor = y_cor
        self.color = color
        self.on_click_method = on_click_method
        self.caption = caption
        self.toggled = False
        self.set_properties_and_create()
        self.caption_obj_instance = self.create_caption()

    def set_properties_and_create(self):
        self.obj_instance.speed(self.speed)
        self.obj_instance.shape(self.shape)
        self.obj_instance.color(self.color)
        self.obj_instance.penup()
        self.obj_instance.goto(self.x_cor, self.y_cor)
        self.obj_instance.shapesize(2,4)
        self.obj_instance.onclick(self.on_click_method)    

    def create_caption(self):
        caption_obj = turtle.Turtle()
        caption_obj.speed(0)
        caption_obj.penup()
        caption_obj.goto(self.x_cor-25, self.y_cor-10)
        caption_obj.pendown()
        caption_obj.write(self.caption)
        caption_obj.hideturtle()
        return caption_obj

    def flicker_button(self, color):
        if not self.toggled:
            self.obj_instance.color(color)
            self.caption_obj_instance.write(self.caption)
            self.toggled = True
        else:
            self.obj_instance.color(self.color)
            self.caption_obj_instance.write(self.caption)
            self.toggled = False     
            
