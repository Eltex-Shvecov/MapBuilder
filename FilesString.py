logo = '''------------------------------------------------------------
--      Created Location-file created by "MapBuilder"     --
------------------------------------------------------------
--      "MapBuilder2" v.0.0 BY SHVETSOV DMITRY	          --
------------------------------------------------------------\n\n'''

enviroment = '''location     = GetCurrentLocation();
SectorData   = CreateSectorDataList();
SectorNumber = GetSectorData (location,SectorData);

environment  = SectorData[SectorNumber].environment;
map_x_size   = SectorData[SectorNumber].map_x_size;
map_y_size   = SectorData[SectorNumber].map_y_size;
music_index  = SectorData[SectorNumber].music_index;


InitMap(map_x_size, map_y_size, 18, 100);
InitEnvironment(environment);
InitMusic(music_index);

SectorData = nil;\n
'''

triggers_portals = '''
-------------------------------------------------------------
--TRIGGERS PORTALS                        
-------------------------------------------------------------
sector_portals  = CreatePortalsInSector();
CreatePortalTriggersOnSector(sector_portals);
TRG_PORTAL_02 = CreateDelay(20,PortalsActivate_Action);
SelectPortalAnimation (GetLastLocation(),mothership);\n'''

triggers_station = '''
-------------------------------------------------------------
--TRIGGERS STATIONS                       
-------------------------------------------------------------
sector_stations = CreateStationsInSector();
CreateStationsTriggersOnSector(sector_stations);\n'''

triggers_inner = '''
-------------------------------------------------------------
--TRIGGERS INNER PORTALS                        
-------------------------------------------------------------
sector_innerportals = CreateInnerPortalsInSector();
CreateInnerPortalTriggersOnSector(sector_innerportals);
TRG_PORTAL_02 = CreateDelay(20,InnerPortalsActivate_Action);\n'''


def Get_LuaComment(str):
    comment = '\n----------------------------------------------------------------\n--' + str.upper() + '\n'
    comment += '----------------------------------------------------------------\n'
    return comment
