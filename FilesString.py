logo = '''------------------------------------------------------------
--      Created Location-file created by "MapBuilder"     --
------------------------------------------------------------
--      "MapBuilder2" v.0.0 BY SHVETSOV DMITRY	          --
------------------------------------------------------------\n\n'''

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