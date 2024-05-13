class Tank:
    def __init__(self):
        self._speed1 = 0
        self._speed2 = 0
        self._tower = 0
        self._light = 0
        self._water = 0
        self._sound = 0
        self._sth = 0

    def get_values(self):
        return [self._speed1, self._speed2, self._tower, self._light, self._water, self._sound, self._sth]

    @property
    def speed1(self):
        return self._speed1

    @property
    def speed2(self):
        return self._speed2

    @property
    def tower(self):
        return self._tower

    @property
    def light(self):
        return self._light

    @property
    def water(self):
        return self._water

    @property
    def sound(self):
        return self._sound

    @property
    def sth(self):
        return self._sth

    @speed1.setter
    def speed1(self, value):
        if -1 <= value <= 1:
            self._speed1 = value
        else:
            raise ValueError("Value of the speed should be in the [-1; 1] interval")

    @speed2.setter
    def speed2(self, value):
        if -1 <= value <= 1:
            self._speed2 = value
        else:
            raise ValueError("Value of the speed should be in the [-1; 1] interval")

    @tower.setter
    def tower(self, value):
        if -1 <= value <= 1:
            self._tower = value
        else:
            raise ValueError("Value of the tower should be in the [-1; 1] interval")

    @light.setter
    def light(self, value):
        if value == 0 or value == 1:
            self._light = value
        else:
            raise ValueError("Value should be 0 or 1")

    @water.setter
    def water(self, value):
        if value == 0 or value == 1:
            self._water = value
        else:
            raise ValueError("Value should be 0 or 1")

    @sound.setter
    def sound(self, value):
        if value == 0 or value == 1:
            self._sound = value
        else:
            raise ValueError("Value should be 0 or 1")

    @sth.setter
    def sth(self, value):
        if value == 0 or value == 1:
            self._sth = value
        else:
            raise ValueError("Value should be 0 or 1")
