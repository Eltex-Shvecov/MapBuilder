# import json
import os
import FilesString as filestr
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
        self._exPortal = False
        self._exStation = False
        self._exIPortal = False

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
        self._bGenerateFiles = tk.Button()
        self._bChangeButton = tk.Button(self._Root, text='Change')


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
        self._bGenerateFiles.config(text='Generate Script file', bd=0, bg='#198cff', fg='white',
                                       activebackground='#19a0ff', font='Arial 16 bold')

        self._bGenerateFiles.config(command=lambda: self.GenerateFiles())
        self._bCreatePortal.config(command=lambda: self.NewObject(type='portal', color='green'))
        self._bCreateStation.config(command=lambda: self.NewObject(type='1', color='red'))
        self._bCreateInnerPortal.config(command=lambda: self.NewObject(type='portal_inner', color='yellow'))
        self._bCreateCarcasses.config(command=lambda: self.NewObject(type='carcasses', color='white'))

        self._bCreatePortal.place_forget()
        self._bCreateStation.place_forget()
        self._bCreateCarcasses.place_forget()
        self._bCreateInnerPortal.place_forget()
        self._bCreatePatrolTruck.place_forget()
        self._bCreateSpaceShip.place_forget()
        self._bGenerateFiles.place_forget()

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
        self._EntryFieldAttributes.place_forget()
        self._bChangeButton.config(command=self.ChangeValueButton)
        self._bChangeButton.place_forget()

        # бинды
        self._Canvas.bind('<MouseWheel>', lambda event: self._Network.resize_network(event, self._Objects))
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
        self._posY = 2000
        self.Set_Title('DEBUG_MAP')
        self._Network.draw_network(self._posX, self._posY)
        self.Visible_button_true()
        self.Visible_TreeView_true()
        self.NewObject(type='portal')

    def Visible_button_true(self):
        """Показать кнопки добавления объектов"""
        self._bCreatePortal.place(anchor='nw', x=1110, y=4, width=115, height=40)
        self._bCreateStation.place(anchor='ne', x=1356, y=4, width=115, height=40)
        self._bCreateInnerPortal.place(anchor='nw', x=1110, y=54, width=115, height=40)
        self._bCreateCarcasses.place(anchor='ne', x=1356, y=54, width=115, height=40)
        self._bCreatePatrolTruck.place(anchor='nw', x=1110, y=104, width=115, height=40)
        self._bCreateSpaceShip.place(anchor='ne', x=1356, y=104, width=115, height=40)
        self._bChangeButton.place(anchor='w', x=1260, y=665, height=22)
        self._EntryFieldAttributes.place(anchor='w', x=1110, y=665, height=20)
        self._bGenerateFiles.place(anchor='se', x=1356, y=765, width=246, height=40)

    def Visible_TreeView_true(self):
        """Показать теблицы данных"""
        self._TreeViewRoot.place(anchor='nw', x=1110, y=154, width=246)
        self._TreeViewConfig.place(anchor='nw', x=1110, y=390, width=246, height=260)

    def RebuildTreeViewConfig(self):
        """Пересоздание таблицы данных объектов"""
        self.ClearTreeViewConfig()
        self._TreeViewConfig.insert('', tk.END, value=('Name', ''))
        self._TreeViewConfig.insert('', tk.END, value=('Type', ''))
        self._TreeViewConfig.insert('', tk.END, value=('Dest loc', ''))
        self._TreeViewConfig.insert('', tk.END, value=('Position', ''), iid='position')
        self._TreeViewConfig.insert('', tk.END, value=('x', ''), iid='1.1')
        self._TreeViewConfig.insert('', tk.END, value=('y', ''), iid='1.2')
        self._TreeViewConfig.insert('', tk.END, value=('z', ''), iid='1.3')
        self._TreeViewConfig.insert('', tk.END, value=('Orientation', ''), iid='orientation')
        self._TreeViewConfig.insert('', tk.END, value=('xx', ''), iid='2.1')
        self._TreeViewConfig.insert('', tk.END, value=('yy', ''), iid='2.2')
        self._TreeViewConfig.insert('', tk.END, value=('zz', ''), iid='2.3')
        self._TreeViewConfig.move('1.1', 'position', '1')
        self._TreeViewConfig.move('1.2', 'position', '1')
        self._TreeViewConfig.move('1.3', 'position', '1')
        self._TreeViewConfig.move('2.1', 'orientation', '1')
        self._TreeViewConfig.move('2.2', 'orientation', '1')
        self._TreeViewConfig.move('2.3', 'orientation', '1')

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

    def NewObject(self, type, color='green'):
        """Создание объекта"""
        if type == 'portal':
            self._exPortal = True
        if type.isdigit():
            self._exStation = True
        if type == 'portal_inner':
            self._exIPortal = True

        if type.isdigit():
            obj = Object('station' + '_' + str(len(self._Objects)), type, color=color)
        else:
            obj = Object(type + '_' + str(len(self._Objects)), type, color=color)

        self._Objects[obj.get_name()] = obj
        self.UpdateTreeViewRoot()

    def UpdateTreeViewRoot(self):
        """Обновление полей в таблице объектов"""
        self.ClearTreeViewRoot()
        for obj in self._Objects.values():
            self._TreeViewRoot.insert('', tk.END, value=[obj.get_name(), obj.get_type()])
        self._Network.draw_network(self._posX, self._posY)
        self._Network.update_draw_objects(self._Objects)

    def UpdateTreeViewConfig(self):
        """Обновление полей в таблице"""
        self.ClearTreeViewConfig()
        for selection in self._TreeViewRoot.selection():
            item = self._TreeViewRoot.item(selection)
            nameObj = item['values'][0]
            obj = self._Objects[str(nameObj)]

            self._TreeViewConfig.insert('', tk.END, value=('Name', obj.get_name()))
            self._TreeViewConfig.insert('', tk.END, value=('Type', obj.get_type()))
            self._TreeViewConfig.insert('', tk.END, value=('Dest loc', obj.get_dest_loc()))
            self._TreeViewConfig.insert('', tk.END, value=('Position', ''), iid='position')
            self._TreeViewConfig.insert('', tk.END, value=('x', obj.get_coordinates()[0]), iid='1.1')
            self._TreeViewConfig.insert('', tk.END, value=('y', obj.get_coordinates()[1]), iid='1.2')
            self._TreeViewConfig.insert('', tk.END, value=('z', obj.get_coordinates()[2]), iid='1.3')
            self._TreeViewConfig.insert('', tk.END, value=('Orientation', ''), iid='orientation')
            self._TreeViewConfig.insert('', tk.END, value=('xx', obj.get_coordinates()[3]), iid='2.1')
            self._TreeViewConfig.insert('', tk.END, value=('yy', obj.get_coordinates()[4]), iid='2.2')
            self._TreeViewConfig.insert('', tk.END, value=('zz', obj.get_coordinates()[5]), iid='2.3')
            self._TreeViewConfig.move('1.1', 'position', '1')
            self._TreeViewConfig.move('1.2', 'position', '1')
            self._TreeViewConfig.move('1.3', 'position', '1')
            self._TreeViewConfig.move('2.1', 'orientation', '1')
            self._TreeViewConfig.move('2.2', 'orientation', '1')
            self._TreeViewConfig.move('2.3', 'orientation', '1')

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
        attr = itemConfig['values'][0]

        if attr == 'Name':
            obj = self._Objects[name]
            obj.change_value(attr, entryValue)
            self._Objects[entryValue] = obj
            del self._Objects[name]
        else:
            obj = self._Objects[name]
            obj.change_value(attr, entryValue)

        self.UpdateTreeViewRoot()
        self.UpdateTreeViewConfig()

    def GenerateFiles(self):
        if self._LocationName is not None:
            if not os.path.exists(self._LocationName):
                os.mkdir(self._LocationName)

            with open(self._LocationName + '/activate.script', 'w') as activate_file:
                activate_file.write(filestr.logo)
                activate_file.write('CountVisitsToSector();\n')

                if self._exPortal:
                    activate_file.write(filestr.triggers_portals)

                if self._exStation:
                    activate_file.write(filestr.triggers_station)

                if self._exIPortal:
                    activate_file.write(filestr.triggers_inner)

            with open(self._LocationName + '/functions.script', 'w') as function_file:
                function_file.write(filestr.logo)
                function_file.write('mothership=GetPlayerMotherShip();\n')
                if self._exPortal:
                    function_file.write('function CreatePortalsInSector()\n')
                    function_file.write('\tsector_portals = {};\n\n')

                    idx = 1
                    for portal in self._Objects.values():
                        if portal.isPortal():
                            function_file.write('\tPortalTemplate(' + str(idx) + ', "P_' + portal.get_name().upper() + '", "' + portal.get_dest_loc().lower() + '");\n')
                            idx += 1

                    function_file.write('\n\treturn sector_portals;\n')
                    function_file.write('end;\n\n')

                if self._exStation:
                    function_file.write('function CreateStationsInSector()\n')
                    function_file.write('\tsector_stations = {};\n\n')

                    idx = 1
                    for station in self._Objects.values():
                        if station.isStation():
                            function_file.write('\tStationTemplate(' + str(idx) + ', "STATION_' + station.get_name().upper() + '", ' + station.get_type() + ', "param", TRUE, {nav_point_prefs});\n')
                            idx += 1

                    function_file.write('\n\treturn sector_stations;\n')
                    function_file.write('end;\n\n')

                if self._exIPortal:
                    function_file.write('function CreateInnerPortalsInSector()\n')
                    function_file.write('\tlocal sector_innerportals = {};\n\n')
                    function_file.write('\treturn sector_innerportals;\n')
                    function_file.write('end;\n')

            with open(self._LocationName + '/location.script', 'w') as location_file:
                location_file.write(filestr.logo)
                location_file.write(filestr.enviroment)
                location_file.write(filestr.Get_LuaComment('cordinates'))

                # Cordinates
                # Портал
                if self._exPortal:
                    for portal in self._Objects.values():
                        if portal.isPortal():
                            location_file.write('XYZ_PORTAL_' + portal.get_name().upper() + ' = Vector3(' + str(portal._x) + ', ' + str(portal._y) + ', ' + str(portal._z) + ');\n')
                # Станция
                if self._exStation:
                    for station in self._Objects.values():
                        if station.isStation():
                            location_file.write('XYZ_' + station.get_name().upper() + '_STATION = Vector3(' + str(station._x) + ', ' + str(station._y) + ', ' + str(station._z) + ');\n')
                # Локальный портал
                if self._exIPortal:
                    for iportal in self._Objects.values():
                        if iportal.isIPortal():
                            location_file.write('XYZ_IPORTAL_' + iportal.get_name().upper() + ' = Vector3(' + str(iportal._x) + ', ' + str(iportal._y) + ', ' + str(iportal._z) + ');\n')

                # Имя
                if self._exPortal:
                    location_file.write(filestr.Get_LuaComment('portals'))
                    for portal in self._Objects.values():
                        if portal.isPortal():
                            location_file.write('PORTAL_' + portal.get_name().upper() + ' = CreateManagedPortal(' + '"' + portal.get_type().lower() + '", "' + portal.get_dest_loc().lower() + '", XYZ_PORTAL_' + portal.get_name().upper() + ', Vector3(' + str(portal._xx) + ', ' + str(portal._yy) + ', ' + str(portal._zz) + '));\n')

                if self._exStation:
                    location_file.write(filestr.Get_LuaComment('stations'))
                    for station in self._Objects.values():
                        if station.isStation():
                            location_file.write(station.get_name().upper() + '_STATION = CreateStation("CARCASSE_NAME", XYZ_' + station.get_name().upper() + '_STATION, Vector3(' + str(station._xx) + ', ' + str(station._yy) + ', ' + str(station._zz) + '));\n')

                if self._exIPortal:
                    location_file.write(filestr.Get_LuaComment('inner portal'))
                    for iportal in self._Objects.values():
                        if iportal.isIPortal():
                            location_file.write('PORTAL_INNER_' + iportal.get_name().upper() + ' = CreateManagedPortal("' + iportal.get_type() + '", "", XYZ_IPORTAL_' + iportal.get_name().upper() + ', Vector3(' + str(iportal._xx) + ', ' + str(iportal._yy) + ', ' + str(iportal._zz) + '));\n')

                # LabelS
                location_file.write(filestr.Get_LuaComment('LabelS'))
                if self._exPortal:
                    for portal in self._Objects.values():
                        if portal.isPortal():
                            location_file.write('SetObjectLabel(PORTAL_' + portal.get_name().upper() + ', "P_' + portal.get_name().upper() + '");\n')

                if self._exStation:
                    for station in self._Objects.values():
                        if station.isStation():
                            location_file.write('SetObjectLabel(' + station.get_name().upper() + '_STATION, "STATION_' + station.get_name().upper() + '");\n')

                if self._exIPortal:
                    for iportal in self._Objects.values():
                        if iportal.isIPortal():
                            location_file.write('SetObjectLabel(PORTAL_INNER_' + portal.get_name().upper() + ', "IP_' + portal.get_name().upper() + '");\n')