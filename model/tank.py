""" A module for saving the current values of the tank.

Represent the part of the model in the MVC. Contains the
current values needed for the tank to operate.

Typical usage:

    tank = Tank()
    tank.get_values()
"""

from typing import List


class Tank:
    """Values of the tank that are needed to operate it.

    All the values that are going to be communicated to
    the tank are stored here.
    """
    def __init__(self) -> None:
        """Initializes the instance."""
        self._left = 0
        self._right = 0
        self._tower_x = 0
        self._tower_y = 0
        self._light = 0
        self._water = 0

    def get_values(self) -> dict:
        """Get the current values of the tank.

        Returns:
            A list of integers representing the current values of the tank.
        """
        return {
            "left_motor": self._left,
            "right_motor": self._right,
            "tower_x": self.tower_x,
            "tower_y": self._tower_y,
            "light": self._light,
            "water": self._water
        }

    @property
    def left(self) -> int:
        """X coordinate of the joystick representing speed and direction."""
        return self._left

    @property
    def right(self) -> int:
        """Y coordinate of the joystick representing speed and direction."""
        return self._right

    @property
    def tower_x(self) -> int:
        """X coordinate of the joystick representing the position of the tank tower."""
        return self._tower_x

    @property
    def tower_y(self) -> int:
        """Y coordinate of the joystick representing the position of the tank tower."""
        return self._tower_y

    @property
    def light(self) -> int:
        """Whether the light are turned on or off."""
        return self._light

    @property
    def water(self) -> int:
        """Whether the water is being shot or not."""
        return self._water

    @left.setter
    def left(self, value: float) -> None:
        """Set the speed1 property.

        Args:
            value (float): The value to set.

        Raises:
            ValueError: If the value is not in the range [-1, 1].
        """
        if -1 <= value <= 1:
            self._left = value
        else:
            raise ValueError("Value of the speed should be in the [-1; 1] interval")

    @right.setter
    def right(self, value: float) -> None:
        """Set the speed2 property.

        Args:
            value (float): The value to set.

        Raises:
            ValueError: If the value is not in the range [-1, 1].
        """
        if -1 <= value <= 1:
            self._right = value
        else:
            raise ValueError("Value of the speed should be in the [-1; 1] interval")

    @tower_x.setter
    def tower_x(self, value: float) -> None:
        """Set the tower_x property.

        Args:
            value (float): The value to set.

        Raises:
            ValueError: If the value is not in the range [-1, 1].
        """
        if -1 <= value <= 1:
            self._tower_x = value
        else:
            raise ValueError("Value of the tower x should be in the [-1; 1] interval")

    @tower_y.setter
    def tower_y(self, value: float) -> None:
        """Set the tower_y property.

        Args:
            value (float): The value to set.

        Raises:
            ValueError: If the value is not in the range [-1, 1].
        """
        if -1 <= value <= 1:
            self._tower_y = value
        else:
            raise ValueError("Value of the tower y should be in the [-1; 1] interval")

    @light.setter
    def light(self, value: int) -> None:
        """Set the light property.

        Args:
            value (int): The value to set.

        Raises:
            ValueError: If the value is not 0 or 1.
        """
        if value in (0, 1):
            self._light = value
        else:
            raise ValueError("Value should be 0 or 1")

    @water.setter
    def water(self, value: int) -> None:
        """Set the water property.

        Args:
            value (int): The value to set.

        Raises:
            ValueError: If the value is not 0 or 1.
        """
        if value in (0, 1):
            self._water = value
        else:
            raise ValueError("Value should be 0 or 1")
