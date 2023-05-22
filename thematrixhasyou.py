import time
import random
import getpass
import tkinter as tk
import tkinter.font as tkfont
import pygetwindow as gw
import pyautogui
import pygame.mixer
import urllib.request
import ctypes

def type_text(widget, text, min_delay=0.06, max_delay=0.12):
    for char in text:
        widget.insert(tk.END, char)
        widget.update()
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)

def disable_input(event):
    return "break"

def close_main_window(root):
    root.destroy()

def play_sound(filepath):
    pygame.mixer.init()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play()

def lock_input():
    # Lock mouse
    ctypes.windll.user32.BlockInput(True)
    # Disable Alt-Tab
    pyautogui.keyDown('alt')

def unlock_input():
    # Unlock mouse
    ctypes.windll.user32.BlockInput(False)
    # Enable Alt-Tab
    pyautogui.keyUp('alt')

def display_matrix(username):
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes('-topmost', True)  # Keep the window on top
    root.attributes('-disabled', True)  # Disable interaction with the window
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.configure(background='black')
    root.config(cursor="none")

    monitors = gw.getAllWindows()
    current_monitor = gw.getActiveWindow()
    target_x = current_monitor.left + current_monitor.width

    pyautogui.FAILSAFE = False
    pyautogui.moveTo(target_x, 0)
    pyautogui.FAILSAFE = True

    main_monitor = None
    for monitor in gw.getAllWindows():
        if "Matrix" in monitor.title:
            main_monitor = monitor
            break

    font_name = "White Rabbit"

    text_widget = tk.Text(root, font=(font_name, 20), fg='green', bg='black', borderwidth=0, highlightthickness=0)
    text_widget.pack(fill=tk.BOTH, expand=True)

    text_widget.config(state=tk.DISABLED)
    text_widget.bind("<Key>", disable_input)

    for monitor in gw.getAllWindows():
        if monitor != main_monitor:
            blank_window = tk.Toplevel(root)
            blank_window.geometry(f"{monitor.width}x{monitor.height}+{monitor.left}+{monitor.top}")
            blank_window.configure(background='black')
            blank_window.overrideredirect(True)

    matrix = [
        f"Wake up, {username}...",
        "The Matrix has you...",
        "Follow the white rabbit."
    ]

    for i, line in enumerate(matrix):
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        type_text(text_widget, line, min_delay=0.2, max_delay=0.35)
        text_widget.config(state=tk.DISABLED)
        time.sleep(5)

    text_widget.config(state=tk.NORMAL)
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, "Knock, knock, " + username + ".")
    text_widget.config(state=tk.DISABLED)
    text_widget.update()

    lock_input()

    root.after(500, lambda: play_sound("knock.mp3"))
    root.after(3500, lambda: unlock_input())
    root.after(4000, lambda: close_main_window(root))

    root.mainloop()

def main():
    username = getpass.getuser()
    display_matrix(username)

if __name__ == "__main__":
    main()
