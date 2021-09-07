import tkinter as tk
from random import *
from tkinter import messagebox

WIDTH = 240
HEIGHT = 240
SEG_SIZE = 20
SCORE = 0

def create_start_coords(): #создаем начальное положение сегмента
    global segments
    x1, y1 = WIDTH/2, HEIGHT/2
    segments = [c.create_rectangle(x1, y1, x1+SEG_SIZE, y1+SEG_SIZE, fill="red"),
                c.create_rectangle(x1, y1+SEG_SIZE, x1+SEG_SIZE, y1+SEG_SIZE*2, fill="white"),
                c.create_rectangle(x1, y1+SEG_SIZE*2, x1+SEG_SIZE, y1+SEG_SIZE*3, fill="white"),]

def create_rand_apple(): #создаем еду для змейки 
    global apple
    
    x1, y1 = randint(0, WIDTH/20 - 1), randint(0, HEIGHT/20 - 1)
    apple_coord = [x1*SEG_SIZE, y1*SEG_SIZE, x1*SEG_SIZE+SEG_SIZE, y1*SEG_SIZE+SEG_SIZE]
    
    for segment in segments: #проверка на колизию со змейкой
        if c.coords(segment) != apple_coord:
            if segment == segments[-1]: #проверяем последний сегмент и выводим яблоко
                apple = c.create_oval(x1*SEG_SIZE, y1*SEG_SIZE, x1*SEG_SIZE+SEG_SIZE, y1*SEG_SIZE+SEG_SIZE, fill="#71db6e")
            continue #продолжаем проверку всех остальних сегментов
        else:
            if len(segments) == (WIDTH/SEG_SIZE)*(HEIGHT/SEG_SIZE):
                tk.messagebox.showwarning("Congratulations", "You are won")
                break
            create_rand_apple()
            break
             
def keyPress(event): #отслеживаем нажатие клавиш
    global segments #выносим список
     
    for segment in segments:
        segment_index = segments.index(segment) #получаем индекс сегмента
        if segment_index == 0: #условие для головы змейки
            x1, y1, x2, y2 = c.coords(segment) #получаем координаты первого сегмента

            if event.keysym == "Up":
                print("Up")
                if y1 == 0:
                    tk.messagebox.showwarning("showwarning", "Warning")
                    break
                c.delete(segments[segment_index]) #удаляем первый сегмент
                segments[segment_index] = c.create_rectangle(x1, y1-SEG_SIZE, x2, y1, fill="red") #переносим первый сегмент
                continue
            elif event.keysym == "Down":
                print("Down")
                if y2 == HEIGHT:
                    tk.messagebox.showwarning("showwarning", "Warning")
                    break
                c.delete(segments[segment_index]) #удаляем первый сегмент
                segments[segment_index] = c.create_rectangle(x1, y2, x2, y2+SEG_SIZE, fill="red") #переносим первый сегмент
                continue
            elif event.keysym == "Left":
                print("Left")
                if x1 == 0:
                    tk.messagebox.showwarning("showwarning", "Warning")
                    break
                c.delete(segments[segment_index]) #удаляем первый сегмент
                segments[segment_index] = c.create_rectangle(x1-SEG_SIZE, y1, x1, y2, fill="red") #переносим первый сегмент
                continue
            elif event.keysym == "Right":
                print("Right")
                if x2 == WIDTH:
                    tk.messagebox.showwarning("showwarning", "Warning")
                    break
                c.delete(segments[segment_index]) #удаляем первый сегмент
                segments[segment_index] = c.create_rectangle(x2, y1, x2+SEG_SIZE, y2, fill="red") #переносим первый сегмент
                continue
            else:
                print(event.keysym)

        current_segmet = (c.coords(segment)) #получаем координаты текущкго сегмента
        c.delete(segments[segment_index])
        segments[segment_index] = c.create_rectangle(x1, y1, x2, y2, fill="white")    
        x1, y1, x2, y2 = current_segmet #присваивем для дальнейшего использования      

    if c.coords(segments[0]) == c.coords(apple): #поедание яблока
        print("Apple:)")
        segments.append(c.create_rectangle(x1, y1, x2, y2, fill="white")) #добавдяем змейке один блок
        c.delete(apple) 
        create_rand_apple()   

def main():
    create_start_coords()
    create_rand_apple()
    c.bind("<Key>", keyPress)
    print('test')

root = tk.Tk()
root.title("Snake")
root.resizable(False, False)

label_score = tk.Label(root, text="Score: {}".format(SCORE), font=('Arial', 40))
label_score.pack()

c = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#42d6cc") #Область игры
c.pack()
c.focus_set()

main()

root.mainloop()

#🛑🛑🛑Змейка не может проходить сквозь себя. Добавить автоматические движения