import tkinter as tk
from random import *
from tkinter import messagebox

WIDTH = 240
HEIGHT = 240
SEG_SIZE = 20
SCORE = 0
DIRECTION = "Up"
access_presskeys = ("Up", "Down", "Left", "Right") #доступные нажатия
count_pressing = 0
access_to_predict = False
pause = False

def start_game_again(): #начинаем игру заново
    global score, DIRECTION, count_pressing, access_to_predict, pause

    c.destroy()
    label_score.destroy()
    label_prompt.destroy()
    SCORE = 0
    DIRECTION = "Up"
    count_pressing = 0
    access_to_predict = False
    pause = False
    main()


def create_start_coords(): #создаем начальное положение сегмента
    global segments
    x1, y1 = WIDTH/2, HEIGHT/2
    segments = [c.create_rectangle(x1, y1, x1+SEG_SIZE, y1+SEG_SIZE, fill="green"),
                c.create_rectangle(x1, y1+SEG_SIZE, x1+SEG_SIZE, y1+SEG_SIZE*2, fill="white"),
                c.create_rectangle(x1, y1+SEG_SIZE*2, x1+SEG_SIZE, y1+SEG_SIZE*3, fill="white"),]

def create_rand_apple(): #создаем еду для змейки 
    global apple
    
    x1, y1 = randint(0, WIDTH/20 - 1), randint(0, HEIGHT/20 - 1)
    apple_coord = [x1*SEG_SIZE, y1*SEG_SIZE, x1*SEG_SIZE+SEG_SIZE, y1*SEG_SIZE+SEG_SIZE]
    
    for segment in segments: #проверка на колизию яблока со змейкой
        if c.coords(segment) != apple_coord:
            if segment == segments[-1]: #проверяем последний сегмент и выводим яблоко
                apple = c.create_oval(x1*SEG_SIZE, y1*SEG_SIZE, x1*SEG_SIZE+SEG_SIZE, y1*SEG_SIZE+SEG_SIZE, fill="#71db6e")
            continue #продолжаем проверку всех остальних сегментов
        else:
            if len(segments) == (WIDTH/SEG_SIZE)*(HEIGHT/SEG_SIZE): #проверяем наличие свободного места
                tk.messagebox.showwarning("Congratulations", "You are win")
                return start_game_again()
            create_rand_apple()
            break

#меняем направление
def tracking_clicks(event): 
    global DIRECTION
    global permission_to_change_direction
    global planned_direction
    global count_pressing
    global pause

    if event.keysym == 'p': #ставим на паузу
        pause = True
        return print('stop game')
    else:
        if pause: #продолжаем игру
            pause = False
            snake_movement()

    for presskey in access_presskeys:  #исключаем другие нажатия
        if event.keysym != presskey:
            if access_presskeys.index(presskey) == len(access_presskeys ) - 1:
                return print("Not available key: {}".format(event.keysym))   
        else:
            break
    
    count_pressing += 1 #подсчитываем количество нажатий
            
    if DIRECTION == "Up" and event.keysym == "Down": #запрет двигаться в противоположную сторону
        pass
    elif DIRECTION == "Down" and event.keysym == "Up":
        pass
    elif DIRECTION == "Left" and event.keysym == "Right":
        pass
    elif DIRECTION == "Right" and event.keysym == "Left":
        pass
    else:
        planned_direction = event.keysym #получаем запланированное направление
        if permission_to_change_direction: #исключаем случайные нажатия клавиш в процесе движения змейки на один блок
            DIRECTION = event.keysym
        permission_to_change_direction = False

#двигаем змейку
def snake_movement(): 
    global segments #выносим список
    global SCORE
    global DIRECTION
    global permission_to_change_direction
    global access_to_predict
    global count_pressing

    if pause:
        return print('The game has been paused')

    if access_to_predict: #меняем запланированное движение
        DIRECTION = planned_direction
        count_pressing = 0
        access_to_predict = False

    if count_pressing > 1: #разрешаем запланированное движение
        access_to_predict = True
    
    for segment in segments:
        segment_index = segments.index(segment) #получаем индекс сегмента
        if segment_index == 0: #условие для головы змейки
            x1, y1, x2, y2 = c.coords(segment) #получаем координаты головы змейки
        
            if DIRECTION == "Up":
                if y1 == 0: #Проверка столкновения со стенкой
                    c.create_rectangle(x1, y1, x2, y2, fill="red")
                    tk.messagebox.showwarning("Losing", "You lose")
                    return start_game_again() 
                
                for segment in segments: #проверка коллизий змейки со змейкой
                    if c.coords(segment) == [x1, y1-SEG_SIZE, x2, y2-SEG_SIZE] and segment != segments[-1]:
                        c.create_rectangle(x1, y1, x2, y2, fill="red")
                        tk.messagebox.showwarning("Losing", "you bumped into yourself")
                        return start_game_again() 
                                                
                c.delete(segments[segment_index]) #удаляем голову змейки
                segments[segment_index] = c.create_rectangle(x1, y1-SEG_SIZE, x2, y1, fill="green") #переносим голову змейки
                continue
            elif DIRECTION == "Down":
                if y2 == HEIGHT: #Проверка столкновения со стенкой
                    c.create_rectangle(x1, y1, x2, y2, fill="red")
                    tk.messagebox.showwarning("Losing", "You lose")
                    return start_game_again() 

                for segment in segments: #проверка коллизий змейки со змейкой
                    if c.coords(segment) == [x1, y1+SEG_SIZE, x2, y2+SEG_SIZE] and segment != segments[-1]:
                        c.create_rectangle(x1, y1, x2, y2, fill="red")
                        tk.messagebox.showwarning("Losing", "you bumped into yourself")
                        return start_game_again()     

                c.delete(segments[segment_index]) #удаляем голову змейки
                segments[segment_index] = c.create_rectangle(x1, y2, x2, y2+SEG_SIZE, fill="green") #переносим голову змейки
                continue
            elif DIRECTION == "Left":
                if x1 == 0: #Проверка столкновения со стенкой
                    c.create_rectangle(x1, y1, x2, y2, fill="red")
                    tk.messagebox.showwarning("Losing", "You lose")
                    return start_game_again() 
                
                for segment in segments: #проверка коллизий змейки со змейкой
                    if c.coords(segment) == [x1-SEG_SIZE, y1, x2-SEG_SIZE, y2] and segment != segments[-1]:
                        c.create_rectangle(x1, y1, x2, y2, fill="red")
                        tk.messagebox.showwarning("Losing", "you bumped into yourself")
                        return start_game_again() 
                        
                c.delete(segments[segment_index]) #удаляем голову змейки
                segments[segment_index] = c.create_rectangle(x1-SEG_SIZE, y1, x1, y2, fill="green") #переносим голову змейки
                continue
            elif DIRECTION == "Right":
                if x2 == WIDTH: #Проверка столкновения со стенкой
                    c.create_rectangle(x1, y1, x2, y2, fill="red")
                    tk.messagebox.showwarning("Losing", "You lose")
                    return start_game_again() 

                for segment in segments: #проверка коллизий змейки со змейкой
                    if c.coords(segment) == [x1+SEG_SIZE, y1, x2+SEG_SIZE, y2] and segment != segments[-1]:
                        c.create_rectangle(x1, y1, x2, y2, fill="red")
                        tk.messagebox.showwarning("Losing", "you bumped into yourself")
                        return start_game_again() 

                c.delete(segments[segment_index]) #удаляем голову змейки
                segments[segment_index] = c.create_rectangle(x2, y1, x2+SEG_SIZE, y2, fill="green") #переносим голову змейки
                continue
            else:
                print(DIRECTION)

        current_segmet = (c.coords(segment)) #получаем координаты текущкго сегмента
        c.delete(segments[segment_index])
        segments[segment_index] = c.create_rectangle(x1, y1, x2, y2, fill="white")    
        x1, y1, x2, y2 = current_segmet #присваивем для дальнейшего использования      

    if c.coords(segments[0]) == c.coords(apple): #поедание яблока
        segments.append(c.create_rectangle(x1, y1, x2, y2, fill="white")) #добавдяем змейке один блок
        c.delete(apple) 
        SCORE += 1
        label_score.config(text="Score: {}".format(SCORE))
        create_rand_apple()

    root.after(200, snake_movement) #делаем, что бы змейка двигалась самостоятельно  
    permission_to_change_direction = True #разрешаем изменить направление

def main():
    def start_game():
        global c, label_score, label_prompt

        game_name_label.destroy()
        game_start_button.destroy()
        label_score = tk.Label(root, text="Score: {}".format(SCORE), font=('Arial', 35))
        label_score.pack()
        c = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#42d6cc") #Область игры
        c.pack()
        c.focus_set()
        label_prompt = tk.Label(root, text="press <p> - stop the game", font=('Arial', 15))
        label_prompt.pack()
        create_start_coords()
        create_rand_apple()
        snake_movement()
        c.bind("<Key>", tracking_clicks)
    
    game_name_label = tk.Label(root, text = "S_n_a_k_e", font=('Arial', 35))
    game_name_label.place(relx=0.09 ,rely=0.1)
    game_start_button = tk.Button(root, text="start game", font=('Arial', 20), command=start_game)
    game_start_button.place(relx=0.24 ,rely=0.5)

root = tk.Tk()
root.geometry('{width}x{height}'.format(width = WIDTH + 50, height = HEIGHT + 100))
root.title("Snake")
root.resizable(False, False)

main()

root.mainloop()

