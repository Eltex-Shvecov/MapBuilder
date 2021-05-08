class Object:

    def __init__(self, name='', x=0, y=0, z=0, xx=0, yy=0, zz=0):
        self._name = name
        self._type = 'portal'
        self._x = x
        self._y = y
        self._z = z
        self._xx = xx
        self._yy = yy
        self._zz = zz

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type

    def set_name(self, name):
        self._name = name

    def change_value(self, attr, value):
        if attr == 'Name':
            self.set_name(value)
