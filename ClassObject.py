class Object:

    def __init__(self, name='', type='portal', x=0, y=0, z=0, xx=0, yy=0, zz=0, dest_loc=''):
        self._name = name
        self._dest_loc = dest_loc
        self._type = type
        self._x = x
        self._y = y
        self._z = z
        self._xx = xx
        self._yy = yy
        self._zz = zz

    def isPortal(self):
        if self._type == 'portal':
            return True
        else:
            return False

    def isStation(self):
        if self._type == 'station':
            return True
        else:
            return False

    def isIPortal(self):
        if self._type == 'portal_inner':
            return True
        else:
            return False

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type

    def get_dest_loc(self):
        return self._dest_loc

    def get_coordinates(self):
        coordinates = [self._x, self._y, self._z, self._xx, self._yy, self._zz]
        return coordinates

    def set_name(self, name):
        self._name = name

    def set_type(self, type):
        self._type = type

    def set_x(self, value):
        self._x = value

    def set_y(self, value):
        self._y = value

    def set_z(self, value):
        self._z = value

    def set_xx(self, value):
        self._xx = value

    def set_yy(self, value):
        self._yy = value

    def set_zz(self, value):
        self._zz = value

    def set_dest_loc(self, value):
        self._dest_loc = value

    def change_value(self, attr, value):
        if attr == 'Name':
            self.set_name(value)
        if attr == 'Type':
            self.set_type(value)
        if attr == 'x':
            self.set_x(value)
        if attr == 'y':
            self.set_y(value)
        if attr == 'z':
            self.set_z(value)
        if attr == 'xx':
            self.set_xx(value)
        if attr == 'yy':
            self.set_yy(value)
        if attr == 'zz':
            self.set_zz(value)
        if attr == 'Dest loc':
            self.set_dest_loc(value)
