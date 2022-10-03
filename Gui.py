###############################################################################
#                                imports                                      #
###############################################################################
import tkinter
from tkinter import *
from tkinter import messagebox
from Game import *
import pygame
import time

###############################################################################
#                                Constant                                     #
###############################################################################

# DIRECTIONS #
UP = '<Up>'
DOWN = '<Down>'
RIGHT = '<Right>'
LEFT = '<Left>'

# FONTS #
LETTERS_FONT = "Yu Gothic UI Semibold"
NUMBERS_FONT = "BN Zarbobim"

# SOUNDS #
MOVE_SOUND = "accompanying files/move_sound.mp3"
GAME_OVER_SOUND = "accompanying files/gameover.wav"
WIN_SOUND = "accompanying files/win.wav"

# VALUES #
BOLD = "bold"
NO = "no"
YES = "yes"
IMG2048 = "accompanying files/2048number.jpg"
FONT = "font"
BG = "bg"
WIDTH = "width"
HEIGHT = "height"
TEXT = "text"

# TEXT #
EMPTY_STR = ""
GAME_NAME = "2048 game"
EXIT = "Exit"
UNDO = "Undo"
REPLAY = "Play again"
SCORE = "Score:\n"
BEST_SCORE = "Best score:\n"
NUM_OF_ROUNDS = "Rounds:\n"
WINNER = "Winner"
LOSER = "The game ended"
YOU_WON = "You won!!"
KEEP_PLAY_Q = "do you want to continue?"
YOU_LOSE = "You lose"
PLAY_AGAIN_Q = "maybe next time..\ndo you want to play again?"

# COLORS #
MAIN_BUTTONS_COLOR = "powder blue"
DATA_BG = "grey45"
BOARD_BG = "grey"
POP_UP_MSG_COLOR = "ivory3"
POP_UP_BUTTON_COLOR = "grey63"
UNDO_PUSHED = "grey57"

# SIZES #
BASE_WIDTH = 400
BASE_HEIGHT = 470
DATA_WIDTH = 400
DATA_HEIGHT = 35
BOARD_WIDTH = 400
BOARD_HEIGHT = 300
BUTTON_WIDTH = 400
BUTTON_HEIGHT = 35
ONE_DATA_WIDTH = 11
ONE_DATA_HEIGHT = 2
ONE_BUTTON_WIDTH = 10
ONE_BUTTON_HEIGHT = 1
CELL_HEIGHT = 1
CELL_WIDTH = 3
NUMBERS_SIZE = 35
LETTERS_SIZE = 15
BIG_LETTERS_SIZE = 20
SMALL_LETTERS_SIZE = 10
BIG_P = 5
MED_P = 2
SMALL_P = 1
POP_MSG_SIZE = "250x150"

###############################################################################
#                                  Class                                      #
###############################################################################


class Gui:

    def __init__(self, root, game_board):
        self.__window = root
        self.__game_board = game_board
        self.__win = False
        self.__window.title(GAME_NAME)
        self.__board_button_index = {}
        self.__data_lst = []
        self.__buttons_lst = []
        self._create_objects()
        self._packing()
        self._create_cells()
        self._display_cells(True)
        self._binding()
        pygame.mixer.init()

    def _create_objects(self):
        """
        create the frames, labels and buttons in the main window
        """
        # frame layers
        self.__base_frame = Frame(self.__window, width=BASE_WIDTH,
                                  height=BASE_HEIGHT)
        self.__data_frame = Frame(self.__base_frame, bg=DATA_BG,
                                  width=DATA_WIDTH, height=DATA_HEIGHT)
        self.__board_frame = Frame(self.__base_frame, bg=BOARD_BG,
                                   width=BOARD_WIDTH, height=BOARD_HEIGHT)
        self.__buttons_frame = Frame(self.__base_frame, width=BUTTON_WIDTH,
                                     height=BUTTON_HEIGHT)

        # label layers
        self.__number2048 = PhotoImage(file=IMG2048)
        self.__title_label = Label(self.__base_frame, image=self.__number2048)
        self.__score_label = Label(self.__data_frame, text=SCORE + str(
            self.__game_board.get_score()))
        self.__best_score_label = Label(self.__data_frame,
                                        text=BEST_SCORE + str(
                                            self.__game_board.get_best_score()))
        self.__num_of_rounds = Label(self.__data_frame,
                                     text=NUM_OF_ROUNDS + str(
                                         self.__game_board.get_num_of_rounds()))
        self.__data_lst.append(self.__score_label)
        self.__data_lst.append(self.__best_score_label)
        self.__data_lst.append(self.__num_of_rounds)

        # buttons
        self.__replay_button = Button(self.__buttons_frame, text=REPLAY,
                                      command=self.play_again)
        self.__exit_button = Button(self.__buttons_frame, text=EXIT,
                                    command=self.__window.destroy)
        self.__undo_button = Button(self.__buttons_frame, text=UNDO,
                                    command=self.undo)
        self.__buttons_lst.append(self.__replay_button)
        self.__buttons_lst.append(self.__exit_button)
        self.__buttons_lst.append(self.__undo_button)

        self.__data_n_buttons_set()
        self.__undo_button[BG] = UNDO_PUSHED

    def __data_n_buttons_set(self):
        """
        auxiliary function for create data labels and buttons
        """
        for layer in self.__data_lst:
            layer[FONT] = (LETTERS_FONT, LETTERS_SIZE, BOLD)
            layer[BG] = MAIN_BUTTONS_COLOR
            layer[WIDTH] = ONE_DATA_WIDTH
            layer[HEIGHT] = ONE_DATA_HEIGHT

        for layer in self.__buttons_lst:
            layer[FONT] = (LETTERS_FONT, LETTERS_SIZE, BOLD)
            layer[BG] = MAIN_BUTTONS_COLOR
            layer[WIDTH] = ONE_BUTTON_WIDTH
            layer[HEIGHT] = ONE_BUTTON_HEIGHT

    def undo(self):
        """
        display the previous board
        """
        self.__game_board.undo()
        self._update_display()
        self.__undo_button[BG] = UNDO_PUSHED

    def _packing(self):
        self.__base_frame.pack()
        self.__title_label.pack()
        self.__data_frame.pack(padx=BIG_P, pady=BIG_P)
        self.__board_frame.pack(padx=BIG_P)
        self.__buttons_frame.pack(padx=BIG_P, pady=BIG_P)
        self.__score_label.pack(side=tkinter.LEFT, padx=MED_P, pady=MED_P)
        self.__best_score_label.pack(side=tkinter.LEFT, pady=MED_P)
        self.__num_of_rounds.pack(side=tkinter.LEFT, padx=MED_P, pady=MED_P)
        self.__replay_button.pack(side=tkinter.LEFT, padx=MED_P, pady=BIG_P)
        self.__exit_button.pack(side=tkinter.LEFT, padx=MED_P, pady=BIG_P)
        self.__undo_button.pack(side=tkinter.LEFT, padx=MED_P, pady=BIG_P)

    def _binding(self):
        self.__window.bind(UP, self._move_up_event)
        self.__window.bind(DOWN, self._move_down_event)
        self.__window.bind(RIGHT, self._move_right_event)
        self.__window.bind(LEFT, self._move_left_event)

    def _move_up_event(self, event):
        self.__game_board.move_up()
        self._any_move_event()

    def _move_down_event(self, event):
        self.__game_board.move_down()
        self._any_move_event()

    def _move_right_event(self, event):
        self.__game_board.move_right()
        self._any_move_event()

    def _move_left_event(self, event):
        self.__game_board.move_left()
        self._any_move_event()

    def _any_move_event(self):
        """
        auxiliary function for the directions functions
        """
        self._update_display()
        if self.__game_board.game_over():
            return self._lose()
        if self.__game_board.winner() and not self.__win:
            return self.win()
        self.__undo_button[BG] = MAIN_BUTTONS_COLOR
        Gui.play_sound(MOVE_SOUND)

    def _update_display(self):
        """
        update every cell and data according to current game board
        """
        self._display_cells(False)
        self.__score_label[TEXT] = SCORE + str(self.__game_board.get_score())
        self.__best_score_label[TEXT] = BEST_SCORE + str(
            self.__game_board.get_best_score())
        self.__num_of_rounds[TEXT] = NUM_OF_ROUNDS + str(
            self.__game_board.get_num_of_rounds())

    def _create_board(self):
        for row in range(ROWS):
            self.__board_frame.rowconfigure(row)
        for column in range(COLS):
            self.__board_frame.columnconfigure(column)

    def _create_cells(self):
        self._create_board()
        for row in range(ROWS):
            for col in range(COLS):
                cell = Label(master=self.__board_frame, height=CELL_HEIGHT,
                             width=CELL_WIDTH,
                             font=(NUMBERS_FONT, NUMBERS_SIZE),
                             bg=self.__game_board.get_cell(row,
                                                           col).get_color())
                self.__board_button_index[cell] = (row, col)

    def _display_cells(self, flag):
        """
        update the board cubes according to the current game board
        """
        for cell in self.__board_button_index:
            row = self.__board_button_index[cell][0]
            col = self.__board_button_index[cell][1]
            cell_val = self.__game_board.get_cell(row, col).get_val()
            cell[TEXT] = cell_val
            if cell_val == 0:
                cell[TEXT] = EMPTY_STR
            cell[BG] = self.__game_board.get_cell(row, col).get_color()
            if flag:
                cell.grid(row=row, column=col, padx=SMALL_P, pady=SMALL_P)

    @staticmethod
    def play_sound(path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

    def _lose(self):
        """
        pop a messagebox in case of game over
        """
        Gui.play_sound(GAME_OVER_SOUND)
        lose_msg = messagebox.askquestion(LOSER, PLAY_AGAIN_Q)
        if lose_msg == YES:
            self.play_again()
        else:
            self.__window.destroy()

    def win(self):
        """
        pop a top level window in case of reaching the win value
        """
        win_msg = Toplevel(self.__window, bg=POP_UP_MSG_COLOR)
        win_msg.title(WINNER)
        win_msg.geometry(POP_MSG_SIZE)
        win_msg_label = Label(win_msg, bg=POP_UP_MSG_COLOR, text=YOU_WON,
                              font=(LETTERS_FONT, BIG_LETTERS_SIZE, BOLD))
        play_again_q = Label(win_msg, bg=POP_UP_MSG_COLOR, text=KEEP_PLAY_Q,
                             font=(LETTERS_FONT, SMALL_LETTERS_SIZE, BOLD))
        buttons_label = Label(win_msg, bg=POP_UP_MSG_COLOR)
        exit_button = Button(buttons_label, text=NO, bg=POP_UP_BUTTON_COLOR,
                             font=(LETTERS_FONT, LETTERS_SIZE, BOLD),
                             command=self.__window.destroy, width=CELL_WIDTH,
                             height=CELL_HEIGHT)
        keep_play_button = Button(buttons_label, text=YES,
                                  bg=POP_UP_BUTTON_COLOR,
                                  font=(LETTERS_FONT, LETTERS_SIZE, BOLD),
                                  command=win_msg.destroy, width=CELL_WIDTH,
                                  height=CELL_HEIGHT)
        win_msg_label.pack()
        play_again_q.pack()
        buttons_label.pack(pady=BIG_P, padx=BIG_P)
        keep_play_button.pack(side=tkinter.LEFT, pady=BIG_P, padx=BIG_P)
        exit_button.pack(side=tkinter.LEFT, pady=BIG_P, padx=BIG_P)
        self.__win = True
        self.play_sound(WIN_SOUND)
        time.sleep(0.7)

    def play_again(self):
        """
        set new game
        """
        self.__game_board.play_again()
        self.__win = False
        self._display_cells(False)
        self.__score_label[TEXT] = SCORE + str(self.__game_board.get_score())
        self.__num_of_rounds[TEXT] = NUM_OF_ROUNDS + str(
            self.__game_board.get_num_of_rounds())

    def start(self):
        self.__window.mainloop()


def main():
    window = Tk()
    game_board = Game()
    gui = Gui(window, game_board)
    gui.start()


if __name__ == '__main__':
    main()
