class Network:

    def __init__(self, canvas, width, height):
        self._rect = None
        self._lines = []
        self._sizeNet = 1
        self._sizeCell = 100
        self._canvas = canvas
        self._center_x = width // 2
        self._center_y = height // 2
        self._x = 0
        self._y = 0
        self._minSize = 0.2
        self._maxSize = 1.7
        self._flagCreated = False

    def draw_network(self, x, y):
        self._canvas.delete('all')
        self._flagCreated = True
        self._x = x
        self._y = y
        x //= self._sizeCell
        y //= self._sizeCell
        x = x // 2 * (self._sizeCell * self._sizeNet)
        y = y // 2 * (self._sizeCell * self._sizeNet)

        x1 = self._center_x - x
        y1 = self._center_y - y
        x2 = self._center_x + x
        y2 = self._center_y + y

        self._rect = self._canvas.create_rectangle(x1, y1, x2, y2, outline='blue')

        # вертикальные линии
        i = self._sizeCell * self._sizeNet
        while i + x1 < x2:
            self._lines.append(self._canvas.create_line(x1 + i, y1, x1 + i, y2, fill='blue'))
            i += self._sizeCell * self._sizeNet

        # горизонтальные линии
        i = self._sizeCell * self._sizeNet
        while i + y1 < y2:
            self._lines.append(self._canvas.create_line(x1, y1 + i, x2, y1 + i, fill='blue'))
            i += self._sizeCell * self._sizeNet

    def resize_network(self, event):
        if self._flagCreated:
            if event.num == 5 or event.delta == -120:
                self._lines.clear()
                if self._sizeNet >= self._minSize:
                    self._sizeNet -= 0.1
                self.draw_network(self._x, self._y)
            if event.num == 4 or event.delta == 120:
                self._lines.clear()
                if self._sizeNet < self._maxSize:
                    self._sizeNet += 0.1
                self.draw_network(self._x, self._y)
