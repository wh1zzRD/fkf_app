from typing import List


class Tank:
    def __init__(self) -> None:
        self._speed1 = 0
        self._speed2 = 0
        self._tower_x = 0
        self._tower_y = 0
        self._light = 0
        self._water = 0
        self._sound = 0
        self._sth = 0

    def get_values(self) -> List[int]:
        return [
            self._speed1,
            self._speed2,
            self._tower_x,
            self._tower_y,
            self._light,
            self._water,
            self._sound,
            self._sth
        ]

    @property
    def speed1(self) -> int:
        return self._speed1

    @property
    def speed2(self) -> int:
        return self._speed2

    @property
    def tower_x(self) -> int:
        return self._tower_x

    @property
    def tower_y(self) -> int:
        return self._tower_y

    @property
    def light(self) -> int:
        return self._light

    @property
    def water(self) -> int:
        return self._water

    @property
    def sound(self) -> int:
        return self._sound

    @property
    def sth(self) -> int:
        return self._sth

    @speed1.setter
    def speed1(self, value: float) -> None:
        if -1 <= value <= 1:
            self._speed1 = value
        else:
            raise ValueError("Value of the speed should be in the [-1; 1] interval")

    @speed2.setter
    def speed2(self, value: float) -> None:
        if -1 <= value <= 1:
            self._speed2 = value
        else:
            raise ValueError("Value of the speed should be in the [-1; 1] interval")

    @tower_x.setter
    def tower_x(self, value: float) -> None:
        if -1 <= value <= 1:
            self._tower_x = value
        else:
            raise ValueError("Value of the tower x should be in the [-1; 1] interval")

    @tower_y.setter
    def tower_y(self, value: float) -> None:
        if -1 <= value <= 1:
            self._tower_y = value
        else:
            raise ValueError("Value of the tower y should be in the [-1; 1] interval")

    @light.setter
    def light(self, value: int) -> None:
        if value in (0, 1):
            self._light = value
        else:
            raise ValueError("Value should be 0 or 1")

    @water.setter
    def water(self, value: int) -> None:
        if value in (0, 1):
            self._water = value
        else:
            raise ValueError("Value should be 0 or 1")

    @sound.setter
    def sound(self, value: int) -> None:
        if value in (0, 1):
            self._sound = value
        else:
            raise ValueError("Value should be 0 or 1")

    @sth.setter
    def sth(self, value: int) -> None:
        if value in (0, 1):
            self._sth = value
        else:
            raise ValueError("Value should be 0 or 1")
