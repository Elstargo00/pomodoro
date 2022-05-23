import tkinter
import time
import pygame

# ---------------------------- CONSTANTS ------------------------------- #

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
CHECK_MARK = "✔"
reps = 0
current_check_mark = ""

# ---------------------------- RINGING ----------------------------------- #

pygame.mixer.init()

def play_sound():
    pygame.mixer.music.load("./vintage_ringtone.wav")
    pygame.mixer.music.play(loops=3)

# ---------------------------- TIMER START/RESET ------------------------------- # 

def start_clicked():
    if reps % 2 == 0:
        timer_label.config(text="WORK", fg=GREEN)
        countdown(WORK_MIN * 60)
    elif reps % 7 == 0:
        timer_label.config(text="BREAK", fg=RED)
        countdown(LONG_BREAK_MIN * 60)
    else:
        timer_label.config(text="BREAK", fg=PINK)
        countdown(SHORT_BREAK_MIN * 60)

def reset_clicked():
    global reps
    global current_check_mark
    current_check_mark = ""
    timer_label.config(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50, "bold"))
    check_label.config(text=f"{current_check_mark}")
    canvas.itemconfig(timer_text, text=time_format(WORK_MIN * 60))
    reps = 0
    
# ---------------------------- TIMER MECHANISM ------------------------------- #

def time_format(t):
    mins, secs = divmod(t, 60)
    timer = '{:02d}:{:02d}'.format(mins, secs)
    return timer

def time_repr(a_time):
    a_time = time_format(a_time)
    canvas.itemconfig(timer_text, text=f"{a_time}")

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def countdown(t):
    global current_check_mark
    global reps

    time_repr(t)
    if t > 0:
        window.after(1000, countdown, t - 1)
    else:
        if reps % 2 == 0:
            current_check_mark += CHECK_MARK
        check_label.config(text=f"{current_check_mark}")
        play_sound()
        reps += 1

# ---------------------------- UI SETUP ------------------------------- #

window = tkinter.Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

timer_label = tkinter.Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50, "bold"))
timer_label.grid(row=0, column=1)

start_button = tkinter.Button(text="Start", command=start_clicked, highlightthickness=0)
start_button.grid(row=2, column=0)

check_label = tkinter.Label(text=current_check_mark, fg=GREEN, bg=YELLOW, font=("Arial", 40, "bold"))
check_label.grid(row=2, column=1)

reset_button = tkinter.Button(text="Reset", command=reset_clicked, highlightthickness=0)
reset_button.grid(row=2, column=2)

canvas = tkinter.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
bg_image = tkinter.PhotoImage(file="./tomato.png")
canvas.create_image(100, 112, image=bg_image)

if reps % 2 == 0:
    timer_text = canvas.create_text(100, 130, text=time_format(WORK_MIN * 60), fill="white", font=("Arial", 35, "bold"))
elif reps % 7 == 0:
    timer_text = canvas.create_text(100, 130, text=time_format(LONG_BREAK_MIN * 60), fill="white", font=("Arial", 35, "bold"))
else:
    timer_text = canvas.create_text(100, 130, text=time_format(SHORT_BREAK_MIN * 60), fill="white", font=("Arial", 35, "bold"))

canvas.grid(row=1, column=1)

window.mainloop()
