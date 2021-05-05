import json
import tkinter as tk
import tkinter.ttk as ttk
from ClassNetwork import Network
from ClassPortal import Portal


class UIApplication:

    def __init__(self, title='', width='1366', height='768'):

        # атрибуты проекта
        self._posX = 0
        self._posY = 0
        self._canvasWidth = 1100
        self._canvasHeight = 762
        self._Portals = []
        self._Stations = []
        self._LocationName = ''
        self._ClearFlag = False
        self._DebugMode = False

        # атрибуты окна
        self._Root = tk.Tk()
        self._Canvas = tk.Canvas(self._Root, width=self._canvasWidth, height=self._canvasHeight, bg='black')
        self._Network = Network(self._Canvas, self._canvasWidth, self._canvasHeight)
        self._WindowName = title
        self._WidthWindow = width
        self._HeightWindow = height
        self._MainMenu = tk.Menu()
        self._DebugMenu = tk.Menu()
        self._ToolsDebugMenu = tk.Menu(tearoff=0)
        self._FileMenu = tk.Menu(tearoff=0)
        self._TreeViewRoot = ttk.Treeview(self._Root, show='headings', columns=('#1', '#2'))
        self._bCreatePortal = tk.Button()
        self._bCreateStation = tk.Button()
        self._bCreateInnerPortal = tk.Button()
        self._bCreateCarcasses = tk.Button()
        self._bCreatePatrolTruck = tk.Button()
        self._bCreateSpaceShip = tk.Button()

    def configuration(self):
        """Конфигурация приложения"""

        # конфигурация окна
        self.Set_Title(self._WindowName)
        self.Set_Size_Window(self._WidthWindow, self._HeightWindow)
        self._Root.config(menu=self._MainMenu)
        self._Canvas.place(anchor='nw', x=2, y=2)
        self._Root.resizable(False, False)

        # конфигурация меню
        self._ToolsDebugMenu.add_command(label='CREATE DEBUG NETWORK', command=self.ClickDEBUG_MAP)
        self._FileMenu.add_command(label='New', command=self.New_Location)
        self._FileMenu.add_command(label='Save', command=self.SaveProject)
        self._MainMenu.add_cascade(label='File', menu=self._FileMenu)
        self._DebugMenu.add_cascade(label='File', menu=self._FileMenu)
        self._DebugMenu.add_cascade(label='Tools', menu=self._ToolsDebugMenu)
        self._FileMenu.add_separator()
        self._FileMenu.add_command(label='Debug Mode ON/OFF', command=self.ChangeDebugMode)

        # конфигурация кнопок создания объектов
        self._bCreatePortal.config(text='Create Portal', bd=0, bg='#198cff', fg='white', activebackground='#19a0ff',
                                   font='Arial 12 bold')
        self._bCreateStation.config(text='Create Station', bd=0, bg='#198cff', fg='white', activebackground='#19a0ff',
                                    font='Arial 12 bold')

        self._bCreateInnerPortal.config(text='Create Inner \nPortal', bd=0, bg='#198cff', fg='white',
                                        activebackground='#19a0ff', font='Arial 12 bold')
        self._bCreateCarcasses.config(text='Create \nCarcasses', bd=0, bg='#198cff', fg='white',
                                      activebackground='#19a0ff', font='Arial 12 bold')

        self._bCreatePatrolTruck.config(text='Create \nPatrol Truck', bd=0, bg='#198cff', fg='white',
                                        activebackground='#19a0ff', font='Arial 12 bold')
        self._bCreateSpaceShip.config(text='Create \nShip(-s)', bd=0, bg='#198cff', fg='white',
                                      activebackground='#19a0ff', font='Arial 12 bold')
        self._bCreatePortal.config(command=self.NewPortal)

        self._bCreatePortal.place_forget()
        self._bCreateStation.place_forget()
        self._bCreateCarcasses.place_forget()
        self._bCreateInnerPortal.place_forget()
        self._bCreatePatrolTruck.place_forget()
        self._bCreateSpaceShip.place_forget()

        # кофигурация таблиц объектов
        self._TreeViewRoot.heading('#1', text='Наименование')
        self._TreeViewRoot.heading('#2', text='Тип')
        self._TreeViewRoot.place(anchor='nw', x=1110, y=154, width=246)
        self._TreeViewRoot.column('#1', width=120)
        self._TreeViewRoot.column('#2', width=120)

        # бинды
        self._Canvas.bind('<MouseWheel>', lambda event: self._Network.resize_network(event))

    def Set_Size_Window(self, x, y):
        self._Root.geometry(x + 'x' + y)

    def Set_Title(self, title):
        self._Root.title(title)

    def StartApplication(self):
        self.configuration()
        self._Root.mainloop()

    def New_Location(self):
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
                                                                               LocationWidth.get(),
                                                                               LocationHeight.get()))
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
        self.Visible_button_true()

        window.destroy()
        window.update()

    # Create DEBUG_MAP
    def ClickDEBUG_MAP(self):
        self._LocationName = 'DEBUG_MAP'
        self._posX = 2000
        self._posY = 1000
        self.Set_Title('DEBUG_MAP')
        self._Network.draw_network(2000, 1000)
        self.Visible_button_true()

    def Visible_button_true(self):
        self._bCreatePortal.place(anchor='nw', x=1110, y=4, width=115, height=40)
        self._bCreateStation.place(anchor='ne', x=1356, y=4, width=115, height=40)
        self._bCreateInnerPortal.place(anchor='nw', x=1110, y=54, width=115, height=40)
        self._bCreateCarcasses.place(anchor='ne', x=1356, y=54, width=115, height=40)
        self._bCreatePatrolTruck.place(anchor='nw', x=1110, y=104, width=115, height=40)
        self._bCreateSpaceShip.place(anchor='ne', x=1356, y=104, width=115, height=40)

    def ChangeDebugMode(self):
        if self._DebugMode:
            self._Root.config(menu=self._MainMenu)
            self._DebugMode = False
            self.Set_Title(self._LocationName)
        else:
            self._Root.config(menu=self._DebugMenu)
            self._DebugMode = True
            self.Set_Title('DEBUG MODE ON')

    def NewPortal(self):
        if self._DebugMode:
            print('New Portal')
        portal = Portal('portal_1', 10, 20, 30)
        self._Portals.append(portal)
        self.FillTreeViewRoot()

    def FillTreeViewRoot(self):
        for i in self._TreeViewRoot.get_children():
            self._TreeViewRoot.delete(i)

        for portal in self._Portals:
            self._TreeViewRoot.insert('', tk.END, value=[portal.get_name(), portal.get_type()])
