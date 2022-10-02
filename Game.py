###############################################################################
#                                imports                                      #
###############################################################################

from copy import deepcopy
from random import seed, randint
import Cell

###############################################################################
#                                Constant                                     #
###############################################################################

COLS = 4
ROWS = 4
INITIAL_VAL1 = 2
INITIAL_VAL2 = 4
GROWTH_RATE = 2
MIN_SCORE_TO_4 = 500
UP = "up"
DOWN = "down"
RIGHT = "right"
LEFT = "left"

###############################################################################
#                                Class                                      #
###############################################################################


class Game:
    def __init__(self):
        # variables initialization
        self.__previous_score = 0
        self.__previous_best_score = 0
        self.__score = 0
        self.__best_score = 0
        self.__num_of_rounds = 0
        seed(1)
        self._board = []
        self.__previous_board = []

        # create initial board
        for i in range(ROWS):
            self._board.append([Cell.Cell(0) for _ in range(COLS)])
        self.random_cell()

    # 4 possible moves functions

    def move_right(self):
        if not self.direction_moves_cells(RIGHT):
            return True
        self.update_previous_board()
        for i in range(ROWS):
            self.zero_cells_move(i, RIGHT, 0, COLS, 1)
            for j in range(COLS - 1, 0, -1):
                if self._board[i][j].get_val() ==\
                        self._board[i][j - 1].get_val():
                    self.same_neighbors(i, j, RIGHT, j - 1, 0, -1)
        self.random_cell()

    def move_left(self):
        if not self.direction_moves_cells(LEFT):
            return True
        self.update_previous_board()
        for i in range(ROWS):
            self.zero_cells_move(i, LEFT, COLS - 1, -1, -1)
            for j in range(COLS - 1):
                if self._board[i][j].get_val() ==\
                        self._board[i][j + 1].get_val():
                    self.same_neighbors(i, j, LEFT, j + 1, COLS - 1, 1)
        self.random_cell()

    def move_up(self):
        if not self.direction_moves_cells(UP):
            return True
        self.update_previous_board()
        for j in range(COLS):
            self.zero_cells_move(j, UP, ROWS - 1, -1, -1)
            for i in range(ROWS - 1):
                if self._board[i][j].get_val() == \
                        self._board[i + 1][j].get_val():
                    self.same_neighbors(i, j, UP, i + 1, ROWS - 1, 1)
        self.random_cell()

    def move_down(self):
        if not self.direction_moves_cells(DOWN):
            return True
        self.update_previous_board()
        for j in range(COLS):
            self.zero_cells_move(j, DOWN, 0, COLS, 1)
            for i in range(ROWS - 1, 0, -1):
                if self._board[i][j].get_val() == \
                        self._board[i - 1][j].get_val():
                    self.same_neighbors(i, j, DOWN, i - 1, 0, -1)
        self.random_cell()

    # auxiliary functions for the moves functions

    def same_neighbors(self, row_idx, col_idx, direction, start, stop, step):
        """
        update the board in case that two identical cell were merged
        :param row_idx: The row index of the cell being merged to
        :param col_idx: The col index of the cell being merged to
        :param direction: the direction of the merging
        :param start: loop start position
        :param stop: loop stop position
        :param step: loop step
        """
        cur_cell = self._board[row_idx][col_idx]
        cur_cell.set_val(cur_cell.get_val() * GROWTH_RATE)
        self.__score += cur_cell.get_val()
        self.__best_score = max(self.__score, self.__best_score)

        if direction == UP or direction == DOWN:
            for k in range(start, stop, step):
                self._board[k][col_idx].\
                    set_val(self._board[k + step][col_idx].get_val())
            self._board[stop][col_idx].set_empty()

        if direction == RIGHT or direction == LEFT:
            for k in range(start, stop, step):
                self._board[row_idx][k].\
                    set_val(self._board[row_idx][k + step].get_val())
            self._board[row_idx][stop].set_empty()

    def zero_cells_move(self, idx, direction, start, stop, step):
        """
        Reduces zeros according to the direction of movement
        :param idx: row idx for right/left and col idx for up/down
        :param direction: the direction of the movement
        :param start: loop start position
        :param stop: loop stop position
        :param step: loop step
        """
        if direction == UP or direction == DOWN:
            for j in range(start, stop, step):
                if self._board[j][idx].get_val() == 0:
                    for k in range(j, start, -step):
                        self._board[k][idx].\
                            set_val(self._board[k - step][idx].get_val())
                    self._board[start][idx].set_empty()

        if direction == RIGHT or direction == LEFT:
            for j in range(start, stop, step):
                if self._board[idx][j].get_val() == 0:
                    for k in range(j, start, -step):
                        self._board[idx][k].\
                            set_val(self._board[idx][k - step].get_val())
                    self._board[idx][start].set_empty()

    def direction_moves_cells(self, direction):
        """
        check if given direction effect the board, doesn't change the board
        :param direction: the direction of the movement
        :return: True if the direction effect the board and False otherwise
        """
        for i in range(ROWS):
            for j in range(COLS):
                cur_val = self._board[i][j].get_val()
                nxt_val = -1
                if direction == DOWN and i != 0:
                    nxt_val = self._board[i - 1][j].get_val()
                if direction == RIGHT and j != 0:
                    nxt_val = self._board[i][j - 1].get_val()
                if direction == UP and i != ROWS - 1:
                    nxt_val = self._board[i + 1][j].get_val()
                if direction == LEFT and j != COLS - 1:
                    nxt_val = self._board[i][j + 1].get_val()
                if nxt_val != -1:
                    if cur_val == nxt_val != 0 or\
                            cur_val == 0 and nxt_val != 0:
                        return True
        return False

    def random_cell(self):
        """
        random index and value for new cell
        """
        idx = randint(0, ROWS*COLS - 1)
        while self._board[idx // COLS][idx % COLS].get_val() != 0:
            idx = randint(0, ROWS * COLS - 1)
        val = randint(0, 1)
        if val and self.__score > MIN_SCORE_TO_4:
            val = INITIAL_VAL2
        else:
            val = INITIAL_VAL1
        self._board[idx // COLS][idx % COLS].set_val(val)

    def update_previous_board(self):
        """
        save the current data before any changes done to allow access to the
        previous board
        """
        self.__previous_board = deepcopy(self._board)
        self.__previous_score = self.__score
        self.__previous_best_score = self.__best_score

    # more optional actions functions

    def undo(self):
        """
        update the current data to previous data if exist
        """
        if not self.__previous_board:
            return
        self._board = self.__previous_board
        self.__score = self.__previous_score
        self.__best_score = self.__previous_best_score
        self.__previous_board = []

    def game_over(self):
        """
        checks if there is no possible moves which mean the game over
        :return: true if game over and false otherwise
        """
        possible_move = self.direction_moves_cells(UP)
        possible_move = possible_move or self.direction_moves_cells(DOWN)
        possible_move = possible_move or self.direction_moves_cells(LEFT)
        possible_move = possible_move or self.direction_moves_cells(RIGHT)
        return not possible_move

    def play_again(self):
        """
        set new game
        """
        self.__score = 0
        self.__num_of_rounds += 1
        for row in self._board:
            for cell in row:
                cell.set_empty()
        self.random_cell()

    # getters and setters

    def get_cell(self, row, col):
        return self._board[row][col]

    def get_cell_val(self, row, col):
        return self._board[row][col].get_val()

    def get_cell_color(self, row, col):
        return self._board[row][col].get_color()

    def get_best_score(self):
        return self.__best_score

    def get_score(self):
        return self.__score

    def get_num_of_rounds(self):
        return self.__num_of_rounds

    def set_cell(self, row, col, val):
        self._board[row][col].set_val(val)

    # inner functions for testing

    def _set_board(self, cpy_brd):
        """
        inner function for set board in tests by lists
        :param cpy_brd: list with the required data in each cell
        """
        # validate check
        if len(cpy_brd) != ROWS:
            raise Exception("length error: invalid rows number")
        for i in range(ROWS):
            if len(cpy_brd[i]) != COLS:
                raise Exception("length error: row", i, "too short")
        # set the board
        for i in range(ROWS):
            for j in range(COLS):
                self.set_cell(i, j, cpy_brd[i][j])

    def _print_board(self):
        """
        inner function for tests
        """
        print("   -board game-   \n##################")
        for i in range(ROWS):
            print("##  ", end="")
            for j in range(COLS):
                print(self._board[i][j].get_val(), end="")
                print("  ", end="")
            print("##")
        print("##################")
