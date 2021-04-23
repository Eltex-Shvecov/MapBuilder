import json
import tkinter as tk
from ClassNetwork import Network


class UIRoot:

    def __init__(self, title, width, height):

        # данные проекта
        self._posX = 0
        self._posY = 0
        self._canvasWidth = 1100
        self._canvasHeight = 762
        self._Portals = []
        self._Stations = []
        self._LocationName = ''
        self._ClearFlag = False


        # данные окна
        self._Root = tk.Tk()
        self._Canvas = tk.Canvas(self._Root, width=self._canvasWidth, height=self._canvasHeight, bg='black')
        self._Network = Network(self._Canvas, self._canvasWidth, self._canvasHeight)
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
        self._FileMenu.add_command(label='Save', command=self.SaveProject)
        self._MainMenu.add_cascade(label='File', menu=self._FileMenu)
        # дебаг кнопка
        self._MainMenu.add_cascade(label='CREATE_DEBUG_MAP', command=self.ClickDEBUG_MAP)

        #бинды
        self._Canvas.bind('<MouseWheel>', lambda event: self._Network.resize_network(event))

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
        ButtonOk.config(width=10, height=1, command=lambda: self.ClickButtonOk(LocationWindow, LocationEntry.get(),
                                                                               LocationWidth.get(), LocationHeight.get()))
        LocationWindow.resizable(False, False)
        LocationEntry.config(font="Arial 14 bold")
        LocationEntry.bind('<Button-1>', lambda event: self.ClearFieldEntry(LocationEntry))

        # Верстка
        LocationWidth.place(anchor='w', x=20, y=70, width=240)
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

    def SaveProject(self):
        if self._LocationName:
            SaveData = {self._LocationName: {}}
            SaveData[self._LocationName]['Portals'] = {}
            SaveData[self._LocationName]['Stations'] = {}
            for i, portal in enumerate(self._Portals):
                SaveData[self._LocationName]['Portals'] = portal
            with open(self._LocationName + '.json', 'w') as FileSave:
                json.dump(SaveData, FileSave)

    def ClickButtonOk(self, window, project_name, pos_x, pos_y):
        self._LocationName = project_name
        self._posX = int(pos_x)
        self._posY = int(pos_y)
        self.Set_Title(project_name)
        self._Network.draw_network(self._posX, self._posY)
        window.destroy()
        window.update()

    # Create DEBUG_MAP
    def ClickDEBUG_MAP(self):
        self.Set_Title('DEBUG_MAP')
        self._Network.draw_network(2000, 1000)