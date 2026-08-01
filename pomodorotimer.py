import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

#the folder .py file lives in 
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

class Pomodoro:
    def __init__(self, root):
        self.root = root

        # tracks whether a countdown is currently active
        # work or break mode
        self.running = False
        self.mode = "work"

        #session counter 
        self.session = 0

    def tick(self, seconds_left, session):
        # if this tick belongs to an old/cancelled timer
        # or if the timer has been stopped, do nothing.
        if session != self.session or not self.running:
            return

        #  minutes and seconds for display 
        minutes, seconds = divmod(seconds_left, 60)
        self.min.set(f"{minutes:02d}")
        self.sec.set(f"{seconds:02d}")

        # countdown finished.
        if seconds_left <= 0:
            self.running = False
            if self.mode == "work":
                messagebox.showinfo("Good Job", "Take a break!\nClick Break to start.")
            else:
                messagebox.showinfo("Time's Up", "Back to work!\nClick Start to begin.")
            return

        # Schedule this same function to run again in 1000ms (1 second),
        # counting down by one second each time. `root.after` is
        # non-blocking, so the rest of the GUI stays responsive while
        # this countdown runs in the background.
        self.root.after(1000, self.tick, seconds_left - 1, session)

    def start_timer(self, total_seconds, mode):
        
        self.mode = mode
        self.running = True

        # Increment session so any previous timer will stop.
        self.session += 1

        self.tick(total_seconds, self.session)

    def work(self):
        self.start_timer(25 * 60, "work")

    def break_(self):
        self.start_timer(5 * 60, "break")


#will create the window and start the GUI event loop
    def main(self):

        self.root.title("Pomodoro Timer")
        self.root.resizable(False, False) 

        #puts jar image into pomodoro timer window 
        img = Image.open(os.path.join(SCRIPT_DIR, "IMG_0500.jpeg"))
        img_w, img_h = img.size

        #will set the image to a max height of 700px, 
        # if the image is larger than that it will scale down to fit
        max_display_height = 700
        if img_h > max_display_height:
            scale = max_display_height / img_h
            img_w, img_h = int(img_w * scale), int(img_h * scale)
            img = img.resize((img_w, img_h), Image.LANCZOS)

        #fail-safe check to ensure the image is in a format Tkinter can handle
        self.bg = ImageTk.PhotoImage(img)

        #resizing the window to match the image dimensions.
        self.root.geometry(f"{img_w}x{img_h}")

        #using a Canvas widget to display the image 
        # and overlay the countdown text on top of it 
        canvas = tk.Canvas(self.root, width=img_w, height=img_h, highlightthickness=0)
        canvas.pack()
        canvas.create_image(0, 0, image=self.bg, anchor="nw")

        #sets the initial countdown time to 25 minutes and 0 seconds
        self.min = tk.StringVar(self.root, value="25")
        self.sec = tk.StringVar(self.root, value="00")

        # text is centered in the jar image 
        box_center_x = 0.50
        box_center_y = 0.62

        text_x = img_w * box_center_x
        text_y = img_h * box_center_y

        #font size setting 
        font_size = max(18, int(img_h * 0.05))

        #just spaces the text apart so it looks nice 
        canvas.create_text(
            text_x, text_y - font_size * 0.6,
            text="", tags="min_text",
            font=("Arial", font_size, "bold"), fill="black"
        )
        
        canvas.create_text(
            text_x, text_y + font_size * 0.6,
            text="", tags="sec_text",
            font=("Arial", font_size, "bold"), fill="black"
        )

        def redraw_time(*_):
            # redraws the countdown text on the canvas whenever the time changes
            canvas.itemconfig("min_text", text=self.min.get())
            canvas.itemconfig("sec_text", text=self.sec.get())

        #resets the countdown 
        self.min.trace_add("write", redraw_time)
        self.sec.trace_add("write", redraw_time)
        redraw_time()  # draw the initial "25:00" immediately

       #button formmating and placement on the window
        btn_y = int(img_h * 0.85)

        tk.Button(
            self.root, text="Start", bd=5, command=self.work,
            bg="red", font=("Arial", 14, "bold")
        ).place(x=img_w * 0.30, y=btn_y)

        tk.Button(
            self.root, text="Break", bd=5, command=self.break_,
            bg="red", font=("Arial", 14, "bold")
        ).place(x=img_w * 0.55, y=btn_y)

        # blocks and keeps the window open until the window closes.
        self.root.mainloop()


# Only runs when this file is executed directly and creates the window 
if __name__ == "__main__":
    pomo = Pomodoro(tk.Tk())  
    pomo.main()
