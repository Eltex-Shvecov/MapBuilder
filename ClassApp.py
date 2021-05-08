# import json
import tkinter as tk
import tkinter.ttk as ttk
from ClassNetwork import Network
from ClassObject import Object


class UIApplication:

    def __init__(self, title='', width='1366', height='768'):

        # атрибуты проекта
        self._posX = 0
        self._posY = 0
        self._canvasWidth = 1100
        self._canvasHeight = 762
        self._Objects = {}
        self._Stations = {}
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
        self._EntryFieldAttributes = tk.Entry(self._Root)
        self._ToolsDebugMenu = tk.Menu(tearoff=0)
        self._FileMenu = tk.Menu(tearoff=0)
        self._TreeViewRoot = ttk.Treeview(self._Root, show='headings', columns=('#1', '#2'))
        self._TreeViewConfig = ttk.Treeview(self._Root, show='tree headings', columns=('#1', '#2'))
        self._ScrollRoot = ttk.Scrollbar(self._Root, orient=tk.VERTICAL, command=self._TreeViewRoot.yview)
        self._bCreatePortal = tk.Button()
        self._bCreateStation = tk.Button()
        self._bCreateInnerPortal = tk.Button()
        self._bCreateCarcasses = tk.Button()
        self._bCreatePatrolTruck = tk.Button()
        self._bCreateSpaceShip = tk.Button()
        self._ChangeButton = tk.Button(self._Root, text='Change')

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
        self._bCreatePortal.config(command=self.NewObject)

        self._bCreatePortal.place_forget()
        self._bCreateStation.place_forget()
        self._bCreateCarcasses.place_forget()
        self._bCreateInnerPortal.place_forget()
        self._bCreatePatrolTruck.place_forget()
        self._bCreateSpaceShip.place_forget()

        # кофигурация таблиц объектов
        self._TreeViewRoot.configure(yscroll=self._ScrollRoot)
        self._TreeViewRoot.heading('#1', text='Name')
        self._TreeViewRoot.heading('#2', text='Type')
        self._TreeViewConfig.heading('#1', text='Attribute')
        self._TreeViewConfig.heading('#2', text='Value')
        self._TreeViewRoot.place_forget()
        self._TreeViewConfig.place_forget()
        self._TreeViewRoot.column('#1', width=115)
        self._TreeViewRoot.column('#2', width=115)
        self._TreeViewConfig.column('#0', width=5)
        self._TreeViewConfig.column('#1', width=95)
        self._TreeViewConfig.column('#2', width=100)
        self._EntryFieldAttributes.place(anchor='w', x=1110, y=665, height=20)
        self._ChangeButton.config(command=self.ChangeValueButton)
        self._ChangeButton.place(anchor='w', x=1260, y=665, height=22)

        # бинды
        self._Canvas.bind('<MouseWheel>', lambda event: self._Network.resize_network(event))
        self._TreeViewRoot.bind('<<TreeviewSelect>>', lambda event: self.UpdateTreeViewConfig())
        self._TreeViewConfig.bind('<<TreeviewSelect>>', lambda event: self.EnterEntryAttributesField(event))

    def Set_Size_Window(self, x, y):
        """Установка размера окна"""
        self._Root.geometry(x + 'x' + y)

    def Set_Title(self, title):
        """Установка заголовка окна"""
        self._Root.title(title)

    def StartApplication(self):
        """Запуск основного цикла"""
        self.configuration()
        self._Root.mainloop()

    def New_Location(self):
        """Окно создания нового проекта"""
        self._ClearFlag = False

        LocationWindow = tk.Toplevel(self._Root)
        LocationWindow.title('New Location')
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
        """Очистка поля названия проекта при фокусе на него"""
        if not self._ClearFlag:
            entry.delete(0, 'end')
            self._ClearFlag = True

    def SaveProject(self):
        # временно убрано из функционала
        pass
        # if self._LocationName:
        # SaveData = {self._LocationName: {}}
        # SaveData[self._LocationName]['Portals'] = {}
        # SaveData[self._LocationName]['Stations'] = {}
        # for i, portal in enumerate(self._Portals):
        # SaveData[self._LocationName]['Portals'] = portal
        # with open(self._LocationName + '.json', 'w') as FileSave:
        # json.dump(SaveData, FileSave)

    def ClickButtonOk(self, window, project_name, pos_x, pos_y):
        """Action по нажатию на кнопку ОК"""
        self._LocationName = project_name
        self._posX = int(pos_x)
        self._posY = int(pos_y)
        self.Set_Title(project_name)
        self._Network.draw_network(self._posX, self._posY)
        self._Objects.clear()
        self._Stations.clear()
        self.ClearTreeViewRoot()
        self.RebuildTreeViewConfig()
        self.Visible_button_true()
        self.Visible_TreeView_true()

        window.destroy()
        window.update()

    def ClickDEBUG_MAP(self):
        """Создание сетки в режиме отладки"""
        self._Objects.clear()
        self._Stations.clear()
        self.ClearTreeViewRoot()
        self.RebuildTreeViewConfig()
        self.Visible_button_true()
        self.Visible_TreeView_true()
        self._LocationName = 'DEBUG_MAP'
        self._posX = 2000
        self._posY = 1000
        self.Set_Title('DEBUG_MAP')
        self._Network.draw_network(2000, 1000)
        self.Visible_button_true()
        self.Visible_TreeView_true()
        self.NewObject()

    def Visible_button_true(self):
        """Показать кнопки добавления объектов"""
        self._bCreatePortal.place(anchor='nw', x=1110, y=4, width=115, height=40)
        self._bCreateStation.place(anchor='ne', x=1356, y=4, width=115, height=40)
        self._bCreateInnerPortal.place(anchor='nw', x=1110, y=54, width=115, height=40)
        self._bCreateCarcasses.place(anchor='ne', x=1356, y=54, width=115, height=40)
        self._bCreatePatrolTruck.place(anchor='nw', x=1110, y=104, width=115, height=40)
        self._bCreateSpaceShip.place(anchor='ne', x=1356, y=104, width=115, height=40)

    def Visible_TreeView_true(self):
        """Показать теблицы данных"""
        self._TreeViewRoot.place(anchor='nw', x=1110, y=154, width=246)
        self._TreeViewConfig.place(anchor='nw', x=1110, y=390, width=246, height=260)

    def RebuildTreeViewConfig(self):
        """Пересоздание таблицы данных объектов"""
        self.ClearTreeViewConfig()
        self._TreeViewConfig.insert('', tk.END, value=('Name', ''))
        self._TreeViewConfig.insert('', tk.END, value=('Type', ''))
        self._TreeViewConfig.insert('', tk.END, value=('Position', ''), iid='1.0')
        self._TreeViewConfig.insert('', tk.END, value=('x', ''), iid='1.1')
        self._TreeViewConfig.insert('', tk.END, value=('y', ''), iid='1.2')
        self._TreeViewConfig.insert('', tk.END, value=('z', ''), iid='1.3')
        self._TreeViewConfig.insert('', tk.END, value=('Orientation', ''), iid='2.0')
        self._TreeViewConfig.insert('', tk.END, value=('x', ''), iid='2.1')
        self._TreeViewConfig.insert('', tk.END, value=('y', ''), iid='2.2')
        self._TreeViewConfig.insert('', tk.END, value=('z', ''), iid='2.3')
        self._TreeViewConfig.move('1.1', '1.0', '1')
        self._TreeViewConfig.move('1.2', '1.0', '1')
        self._TreeViewConfig.move('1.3', '1.0', '1')
        self._TreeViewConfig.move('2.1', '2.0', '1')
        self._TreeViewConfig.move('2.2', '2.0', '1')
        self._TreeViewConfig.move('2.3', '2.0', '1')

    def ClearTreeViewRoot(self):
        """Очистка полей в таблице объектов"""
        for i in self._TreeViewRoot.get_children():
            self._TreeViewRoot.delete(i)

    def ClearTreeViewConfig(self):
        """Очистка полей в таблице данных"""
        for i in self._TreeViewConfig.get_children():
            self._TreeViewConfig.delete(i)

    def ChangeDebugMode(self):
        """Смена режима отладки"""
        if self._DebugMode:
            self._Root.config(menu=self._MainMenu)
            self._DebugMode = False
            self.Set_Title(self._LocationName)
        else:
            self._Root.config(menu=self._DebugMenu)
            self._DebugMode = True
            self.Set_Title('DEBUG MODE ON')

    def NewObject(self):
        """Создание объекта"""
        obj = Object('portal_' + str(len(self._Objects)))
        self._Objects[obj.get_name()] = obj
        self.UpdateTreeViewRoot()

    def UpdateTreeViewRoot(self):
        """Обновление полей в таблице объектов"""
        self.ClearTreeViewRoot()
        for obj in self._Objects.values():
            self._TreeViewRoot.insert('', tk.END, value=[obj.get_name(), obj.get_type()])

    def UpdateTreeViewConfig(self):
        """Обновление полей в таблице"""
        self.ClearTreeViewConfig()
        for selection in self._TreeViewRoot.selection():
            item = self._TreeViewRoot.item(selection)
            nameObj = item['values'][0]
            obj = self._Objects[str(nameObj)]

            self._TreeViewConfig.insert('', tk.END, value=('Name', obj.get_name()))
            self._TreeViewConfig.insert('', tk.END, value=('Type', obj.get_type()))
            self._TreeViewConfig.insert('', tk.END, value=('Position', ''), iid='1.0')
            self._TreeViewConfig.insert('', tk.END, value=('x', obj._x), iid='1.1')
            self._TreeViewConfig.insert('', tk.END, value=('y', obj._y), iid='1.2')
            self._TreeViewConfig.insert('', tk.END, value=('z', obj._z), iid='1.3')
            self._TreeViewConfig.insert('', tk.END, value=('Orientation', ''), iid='2.0')
            self._TreeViewConfig.insert('', tk.END, value=('x', ''), iid='2.1')
            self._TreeViewConfig.insert('', tk.END, value=('y', ''), iid='2.2')
            self._TreeViewConfig.insert('', tk.END, value=('z', ''), iid='2.3')
            self._TreeViewConfig.move('1.1', '1.0', '1')
            self._TreeViewConfig.move('1.2', '1.0', '1')
            self._TreeViewConfig.move('1.3', '1.0', '1')
            self._TreeViewConfig.move('2.1', '2.0', '1')
            self._TreeViewConfig.move('2.2', '2.0', '1')
            self._TreeViewConfig.move('2.3', '2.0', '1')

    def EnterEntryAttributesField(self, event):
        self._EntryFieldAttributes.delete(0, tk.END)
        item = self._TreeViewConfig.item(self._TreeViewConfig.selection()[0])
        if item is not None:
            value = item['values'][1]
            self._EntryFieldAttributes.insert(0, value)

    def ChangeValueButton(self):
        entryValue = self._EntryFieldAttributes.get()
        itemRoot = self._TreeViewRoot.item(self._TreeViewRoot.selection()[0])
        itemConfig = self._TreeViewConfig.item(self._TreeViewConfig.selection()[0])
        name = itemRoot['values'][0]
        type = itemRoot['values'][1]
        attr = itemConfig['values'][0]

        if type == 'portal':
            obj = self._Objects[name]
            obj.change_value(attr, entryValue)
            self._Objects[entryValue] = obj
            del self._Objects[name]

        self.UpdateTreeViewRoot()
        self.UpdateTreeViewConfig()
