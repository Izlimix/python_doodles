#!/usr/bin/env python3

import time

class Duration:
    sec = 1
    ms = sec / 1000
    minute = 60 * sec
    hr = 60 * minute
    day = 24 * hr
    
#Doodle for leety
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
# End Doodle    

def main():
    #do stuff
    # Initialise everything
    # Set up + Draw the main menu
    # Main loop: Wait for input, update screen, repeat.
    # Timer loop: Every time unit (1 ms resolution?) update current time, check and resolve events, check for new inputs? (or do this is another thread)
    draw()
    pass

# Will eventually drift, since event() and checking the condition take non-negligible time
def bad_timer(event, resolution=Duration.sec, end_condition=False):
    while not end_condition :
        time.sleep(resolution)
        event()
        
def interpret(command):
    # I wish pattern matching was a thing in this version
    pass
    
        
def draw():
    print("_" * 50)
    print(f"Redrawn at: {time.asctime()}")
    print(f"Or Unix time in seconds: {time.time()}")
    pass
    

if __name__ == "__main__":
    main()