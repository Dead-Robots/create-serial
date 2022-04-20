from createserial.commands import read_create_encoders


class Encoders:
    """Represents the encoders of the Create and handles value wraparound"""

    def __init__(self):
        self.__prev_left, self.__prev_right = self.__get_raw()
        self.__left = self.__right = 0

    @property
    def values(self):
        """The left and right encoder values relative to the robot's start"""
        left, right = self.__get_raw()
        adjusted_left = self.__adjust(left, self.__prev_left)
        adjusted_right = self.__adjust(right, self.__prev_right)
        self.__prev_left, self.__prev_right = left, right
        self.__left += adjusted_left
        self.__right += adjusted_right
        return self.__left, self.__right

    def reset(self):
        """Reset the values back to 0"""
        self.__init__()

    @staticmethod
    def __adjust(value, prev):
        if abs(value - prev) > 32768:
            value = value + 65536 if value < 32768 else value - 65536
        return value - prev

    @staticmethod
    def __get_raw():
        return read_create_encoders()
