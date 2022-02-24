import tkinter as tk

class ParagraphComparissonWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('Paragraph comparisson')

        # configure geometry
        # window width and height
        window_width = 700
        window_height = 600

        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{100}+{100}')

        # setting a minimum and maximum size of the window
        self.minsize(window_width, window_height)