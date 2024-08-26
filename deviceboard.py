from turtle import Turtle

class Deviceboard(Turtle):
    def __init__(self):
        super().__init__()
        self.selected_device1 = ''
        self.selected_device2 = ''
        self.speed(0)
        self.hideturtle()
        self.penup()
        self.x_cor = 550
        self.y_cor = 400
        self.goto(self.x_cor, self.y_cor)
        self.write('Device Connection Stats')

    def updateBoard(self, content):
        self.y_cor -= 15
        self.goto(self.x_cor, self.y_cor)
        self.write(content)


