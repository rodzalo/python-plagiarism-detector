from views.appWindow import App
from views.controlFrame import ControlFrame

if __name__ == "__main__":
    app = App()
    frame = ControlFrame(app)
    app.mainloop()
    