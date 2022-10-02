from copy import deepcopy
from random import seed
from random import randint
import Cell

COLS = 4
ROWS = 4
INITIAL_VAL1 = 2
INITIAL_VAL2 = 4
MIN_SCORE_TO_4 = 500
UP = "up"
DOWN = "down"
RIGHT = "right"
LEFT = "left"


class Game:
    def __init__(self):
        self._score = 0
        self.__previous_score = 0
        self.__previous_best_score = 0
        self._best_score = 0
        self._num_of_rounds = 0
        seed(1)
        self._board = []
        self.__previous_board = []
        for i in range(ROWS):
            self._board.append([Cell.Cell(0) for i in range(COLS)])
        self.random_cell()

    def move_right(self):
        if not self.direction_moves_cells(RIGHT):
            return True
        self.__previous_board = deepcopy(self._board)
        self.__previous_score = self._score
        self.__previous_best_score = self._best_score
        for i in range(ROWS):
            self.zero_cells_move(i, RIGHT, 0, COLS, 1)
            for j in range(COLS - 1, 0, -1):
                if self._board[i][j].get_val() ==\
                        self._board[i][j - 1].get_val():
                    self.same_neighbors(i, j, RIGHT, j - 1, 0, -1)
        return self.random_cell()

    def move_left(self):
        if not self.direction_moves_cells(LEFT):
            return True
        self.__previous_board = deepcopy(self._board)
        self.__previous_score = self._score
        self.__previous_best_score = self._best_score
        for i in range(ROWS):
            self.zero_cells_move(i, LEFT, COLS - 1, -1, -1)
            for j in range(COLS - 1):
                if self._board[i][j].get_val() ==\
                        self._board[i][j + 1].get_val():
                    self.same_neighbors(i, j, LEFT, j + 1, COLS - 1, 1)
        return self.random_cell()

    def move_up(self):
        if not self.direction_moves_cells(UP):
            return True
        self.__previous_score = self._score
        self.__previous_best_score = self._best_score
        self.__previous_board = deepcopy(self._board)
        for j in range(COLS):
            self.zero_cells_move(j, UP, ROWS - 1, -1, -1)
            for i in range(ROWS - 1):
                if self._board[i][j].get_val() == \
                        self._board[i + 1][j].get_val():
                    self.same_neighbors(i, j, UP, i + 1, ROWS - 1, 1)
        return self.random_cell()

    def move_down(self):
        if not self.direction_moves_cells(DOWN):
            return True
        self.__previous_board = deepcopy(self._board)
        self.__previous_score = self._score
        self.__previous_best_score = self._best_score
        for j in range(COLS):
            self.zero_cells_move(j, DOWN, 0, COLS, 1)
            for i in range(ROWS - 1, 0, -1):
                if self._board[i][j].get_val() == \
                        self._board[i - 1][j].get_val():
                    self.same_neighbors(i, j, DOWN, i - 1, 0, -1)
        return self.random_cell()

    def same_neighbors(self, row_idx, col_idx, direction, start, stop, step):
        cur_cell = self._board[row_idx][col_idx]
        cur_cell.set_val(cur_cell.get_val() * 2)
        self._score += cur_cell.get_val()
        self._best_score = max(self._score, self._best_score)

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

    def undo(self):
        if not self.__previous_board:
            return
        self._board = self.__previous_board
        self._score = self.__previous_score
        self._best_score = self.__previous_best_score
        self.__previous_board = []

    def zero_cells_move(self, idx, direction, start, stop, step):
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

    def get_cell(self, row, col):
        return self._board[row][col]

    def get_cell_val(self, row, col):
        return self._board[row][col].get_val()

    def get_cell_color(self, row, col):
        return self._board[row][col].get_color()

    def get_best_score(self):
        return self._best_score

    def get_score(self):
        return self._score

    def get_num_of_rounds(self):
        return self._num_of_rounds

    def game_over(self):
        possible_move = self.direction_moves_cells(UP)
        possible_move = possible_move or self.direction_moves_cells(DOWN)
        possible_move = possible_move or self.direction_moves_cells(LEFT)
        possible_move = possible_move or self.direction_moves_cells(RIGHT)
        return not possible_move

    def replay(self):
        self._score = 0
        self._num_of_rounds += 1
        for row in self._board:
            for cell in row:
                cell.set_empty()
        self.random_cell()

    def set_cell(self, row, col, val):
        self._board[row][col].set_val(val)

    def _set_board(self, cpy_brd):
        # if len(cpy_brd) != ROWS:
        #     # TODO ERROR
        # for i in range(ROWS):
        #     if len(cpy_brd[i]) != COLS:
        #         # TODO ERROR
        for i in range(ROWS):
            for j in range(COLS):
                self.set_cell(i, j, cpy_brd[i][j])

    def random_cell(self):
        if self.board_full():
            return False
        idx = randint(0, ROWS*COLS - 1)
        while self._board[idx // COLS][idx % COLS].get_val() != 0:
            idx = randint(0, ROWS * COLS - 1)
        val = randint(0, 1)
        if val and self._score > MIN_SCORE_TO_4:
            val = INITIAL_VAL2
        else:
            val = INITIAL_VAL1
        self._board[idx // COLS][idx % COLS].set_val(val)
        return True

    def board_full(self):
        for row in self._board:
            for cell in row:
                if cell.get_val() == 0:
                    return False
        return True

    def _print_board(self):
        print("   -board game-   \n##################")
        for i in range(ROWS):
            print("##  ", end="")
            for j in range(COLS):
                print(self._board[i][j].get_val(), end="")
                print("  ", end="")
            print("##")
        print("##################")
