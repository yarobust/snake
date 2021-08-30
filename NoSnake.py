import tkinter as tk
from random import *

root = tk.Tk()
root.title("Snake")

c = tk.Canvas(root, width=700, height=700, bg="#42d6cc")
c.pack()
c.focus_set()


def create_rand_coords():
    global last_seg
    x1 = randint(0, 34)
    y1 = randint(0, 34)
    print(x1, y1)
    last_seg = c.create_rectangle(x1*20, y1*20, x1*20+20, y1*20+20, fill="white")
    

def keyPress(event):
    global last_seg
    print(c.coords(last_seg))
    x1, y1, x2, y2 = c.coords(last_seg)
    c.delete(last_seg)
    if event.keysym == "Up":
        print("Up")
        first_seg = c.create_rectangle(x1, y1-20, x2, y2-20, fill="white")
    elif event.keysym == "Down":
        print("Down")
        first_seg = c.create_rectangle(x1, y1+20, x2, y2+20, fill="white")
    elif event.keysym == "Right":
        print("Right")
        first_seg = c.create_rectangle(x1+20, y1, x2+20, y2, fill="white")
    elif event.keysym == "Left":
        print("Left")
        first_seg = c.create_rectangle(x1-20, y1, x2-20, y2, fill="white")
    else:
        print(event.keysym)
    last_seg = first_seg    
    
create_rand_coords()
print(last_seg)

c.bind("<Key>", keyPress)


root.mainloop()
