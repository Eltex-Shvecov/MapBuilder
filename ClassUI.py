import tkinter as tk


class UIRoot:

    def __init__(self, title, width, height):
        self._Root = tk.Tk()
        self._Canvas = tk.Canvas(self._Root, width=1100, height=762, bg='black')

        self._Portals = []
        self._Stations = []
        self._LocationName = ''
        self._ClearFlag = False

        self._WindowName = title
        self._WidthWindow = width
        self._HeightWindow = height
        self._MainMenu = tk.Menu(self._Root)
        self._FileMenu = tk.Menu(self._MainMenu, tearoff=0)

    def configuration(self):
        """Конфигурация приложения"""

        # конфигурация окна
        self.Set_Title(self._WindowName)
        self.Set_Size_Window(self._WidthWindow, self._HeightWindow)
        self._Root.config(menu=self._MainMenu)
        self._Canvas.place(anchor='nw', x=2, y=2)
        self._Root.resizable(False, False)

        # конфигурация меню
        self._FileMenu.add_command(label='New', command=self.New_Location)
        self._MainMenu.add_cascade(label='File', menu=self._FileMenu)

    def Set_Size_Window(self, x, y):
        self._Root.geometry(x + 'x' + y)

    def Set_Title(self, title):
        self._Root.title(title)

    def ShowWindow(self):
        self.configuration()
        self._Root.mainloop()

    def New_Location(self):
        print('New Location')
        self._ClearFlag = False
        LocationWindow = tk.Toplevel(self._Root)
        ButtonOk = tk.Button(LocationWindow, text='Ok')
        LocationEntry = tk.Entry(LocationWindow)
        LocationWidth = tk.Entry(LocationWindow)
        LocationHeight = tk.Entry(LocationWindow)

        # конфигурация
        LocationWidth.config(font="Arial 14 bold")
        LocationHeight.config(font="Arial 14 bold")
        LocationWindow.geometry('540x150')
        LocationWindow.config(bg='#ADDBE2')
        ButtonOk.config(width=10, height=1)
        LocationWindow.resizable(False, False)
        LocationEntry.config(font="Arial 14 bold")
        LocationEntry.bind('<Button-1>', lambda event: self.ClearFieldEntry(LocationEntry))

        # Верстка
        LocationWidth.place(anchor='w',  x=20, y=70, width=240)
        LocationHeight.place(anchor='e', x=520, y=70, width=240)
        ButtonOk.place(anchor='center', x=475, y=125)
        LocationEntry.place(anchor='center', relx=0.5, y=30, width=500)

        LocationEntry.insert(0, "Enter location name")
        LocationWidth.insert(0, 'posX')
        LocationHeight.insert(0, 'posY')

    def ClearFieldEntry(self, entry):
        if not self._ClearFlag:
            entry.delete(0, 'end')
            self._ClearFlag = True
