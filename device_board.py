import turtle

class DeviceBoard():
    def __init__(self):
        self.obj_instance = turtle.Turtle()
        self.obj_instance.hideturtle()
        self.starting_device = None
        self.ending_device = None

    def display(self, starting_device = None, ending_device = None):
        self.starting_device = starting_device
        self.ending_device = ending_device
        self.obj_instance.clear()
        self.obj_instance.speed(0)
        self.obj_instance.penup()
        self.obj_instance.goto(-30, 400)
        self.obj_instance.write(f'Starting Device: {self.starting_device}\nEnding Device: {self.ending_device}', font=("Arial", 8, 'normal', 'bold'))

    def stop_displaying(self):
        self.obj_instance.clear()