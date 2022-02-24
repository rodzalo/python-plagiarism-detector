import tkinter as tk

VERSION = 'v1.0.0'
AUTHOR = "rodzalo"

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title(f'Python Plagiarism Detector {VERSION} - github.com/{AUTHOR}')

        # configure geometry
        # window width and height
        window_width = 600
        window_height = 600

        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # setting a minimum and maximum size of the window
        self.minsize(window_width, window_height)