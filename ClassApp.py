from ClassUI import UIRoot


class Application:

    def __init__(self):
        self._UIRoot = UIRoot('Map  Builder v1.0 Alpha', '1366', '768')

    def startApp(self):
        self._UIRoot.ShowWindow()

    def AddPortal(self, portal):
        self._Portals.append(portal)

    def AddStation(self, station):
        self._Stations.append(station)

    def Set_Project_Name(self, name):
        self._LocationName = name
