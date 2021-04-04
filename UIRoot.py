import tkinter as tk


class UIRoot:

    def __init__(self):
        self.root = tk.Tk()

    def configuration(self):
        """Конфигурация окна"""
        self.root.geometry('1280x720')
        self.root.title('Map Builder')

    def start_application(self):
        self.configuration()
        self.root.mainloop()
