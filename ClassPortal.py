class Portal:

    def __init__(self, name='', x=0, y=0, z=0):
        self._name = name
        self._type = 'PORTAL'
        self._x = x
        self._y = y
        self._z = z

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type
