# Doodle for leety
# Done for a friend new to coding, who needed help with a timer project.
# Snippet for use in her project in the Python2 version of codeskulptor https://py2.codeskulptor.org/

class Light:
    status_colours = {
        "break": "skyblue",
        "work": "red",
        "off": "grey",
        "selected": "yellow"
    }

    def __init__(self, pos, status):
        self.pos = pos
        self.status = status
        pass

    def draw(self, canvas):
        # Draw a circle of the colour corresponding to this light's status at this light's position
        colour = status_colours[self.status]
        canvas.draw_circle(self.pos, 7.5, 1, "black", colour)
    # Plus more in the codeskulptor link that was sent~

class Task:
    def __init__(self, name, car_colour, car_outline):
        self.name = name
        self.car_colour = car_colour
        self.car_outline = car_outline
        self.pos = 0 #initial position/angle?
        # self.end_time = 100 #if you want to keep track of the time remaining per task, for example? Could be a parameter like name

    def draw(self, canvas):
        # canvas.draw_circle( ... based on self.car_colour and outline and pos?)

# When creating a task, add it to the list of all tasks at the end by appending it to your task list
# e.g.
#   tasks = []
#   tasks.append(Task("Potato", "blue", "black"))
# Then you can draw each task and update each one appropriately
#  for task in tasks:
#     task.draw(canvas)
#     task.pos += 1 #for example
# And when a task is complete, just delete it from the tasks list (prob by index)
#   del task[4]

# End Doodle
