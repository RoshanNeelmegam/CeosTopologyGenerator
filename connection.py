import turtle

class Connection():
    def __init__(self, starting_points, ending_points):
        self.starting_points = starting_points
        self.ending_points = ending_points

    def create(self):
        line = turtle.Turtle()
        line.speed(0)
        line.hideturtle()
        line.penup()
        line.goto(self.starting_points)
        line.pendown()
        line.goto(self.ending_points)
        line.penup()
        line.hideturtle()
 