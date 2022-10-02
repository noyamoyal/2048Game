MAX_POWER = 12
COLORS_LIST = ["LightYellow3", "LightCyan2", "LightSteelBlue2", "cadet blue",
               "dark sea green", "medium aquamarine", "PaleGreen2",
               "sea green", "DarkOliveGreen3", "pink3", "goldenrod",
               "coral2", "DarkSlateGray3"]


class Cell:
    colors_dict = {}
    if len(COLORS_LIST) != MAX_POWER + 1:
        pass
        # TODO ERROR
    colors_dict[0] = COLORS_LIST[0]
    for i in range(1, MAX_POWER + 1):
        colors_dict[2**i] = COLORS_LIST[i]

    def __init__(self, val):
        self.__value = val
        self.__color = Cell.colors_dict[val]

    def set_val(self, val):
        self.__value = val
        self.__color = Cell.colors_dict[val]

    def set_empty(self):
        self.set_val(0)

    def get_val(self):
        return self.__value

    def get_color(self):
        return self.__color

