###############################################################################
#                                Constant                                     #
###############################################################################

MAX_POWER = 12
COLORS_LIST = ["LightYellow3", "LightCyan2", "LightSteelBlue2", "cadet blue",
               "dark sea green", "medium aquamarine", "PaleGreen2",
               "sea green", "DarkOliveGreen3", "pink3", "goldenrod",
               "coral2", "DarkSlateGray3"]
INVALID_DATA_MSG = "invalid data: unmatch max power and color list's length"
GROWTH_RATE = 2


###############################################################################
#                                Class                                      #
###############################################################################


class Cell:
    # validity check
    if len(COLORS_LIST) != MAX_POWER + 1:
        raise Exception(INVALID_DATA_MSG)

    # static dictionary definition
    colors_dict = {0: COLORS_LIST[0]}
    for i in range(1, MAX_POWER + 1):
        colors_dict[GROWTH_RATE**i] = COLORS_LIST[i]

    def __init__(self, val):
        self.__value = val
        self.__color = Cell.colors_dict[val]

    # getters and setters

    def get_val(self):
        return self.__value

    def get_color(self):
        return self.__color

    def set_val(self, val):
        self.__value = val
        self.__color = Cell.colors_dict[val]

    def set_empty(self):
        self.set_val(0)
