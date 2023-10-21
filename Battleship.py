# Author: Yingtong Deng
# Battleship
# Date due: 2020-12-04

import random

### DO NOT EDIT BELOW (with the exception of MAX_MISSES) ###

HIT_CHAR = 'x'
MISS_CHAR = 'o'
BLANK_CHAR = '.'
HORIZONTAL = 'h'
VERTICAL = 'v'
MAX_MISSES = 20
SHIP_SIZES = {
    "carrier": 5,
    "battleship": 4,
    "cruiser": 3,
    "submarine": 3,
    "destroyer": 2
}
NUM_ROWS = 10
NUM_COLS = 10
ROW_IDX = 0
COL_IDX = 1
MIN_ROW_LABEL = 'A'
MAX_ROW_LABEL = 'J'


def get_random_position():
    """Generates a random location on a board of NUM_ROWS x NUM_COLS."""

    row_choice = chr(
        random.choice(
            range(
                ord(MIN_ROW_LABEL),
                ord(MIN_ROW_LABEL) + NUM_ROWS
            )
        )
    )

    col_choice = random.randint(0, NUM_COLS - 1)

    return row_choice, col_choice


def play_battleship():
    """Controls flow of Battleship games including display of
    welcome and goodbye messages.

    :return: None
    """

    print("Let's Play Battleship!\n")

    game_over = False

    while not game_over:
        game = Game()
        game.display_board()

        while not game.is_complete():
            pos = game.get_guess()
            result = game.check_guess(pos)
            game.update_game(result, pos)
            game.display_board()

        game_over = end_program()

    print("Goodbye.")


### DO NOT EDIT ABOVE (with the exception of MAX_MISSES) ###


class Ship:

    def __init__(self, name, start_position, orientation):
        """Creates a new ship with the given name, placed at start_position in the
        provided orientation. The number of positions occupied by the ship is determined
        by looking up the name in the SHIP_SIZE dictionary.

        :param name: the name of the ship
        :param start_position: tuple representing the starting position of ship on the board
        :param orientation: the orientation of the ship ('v' - vertical, 'h' - horizontal)
        :return: None
        """
        self.positions = {} # battleship board of the game that records ship position from users
        self.name = name
        number_of_positions = SHIP_SIZES[name]
        self.sunk = False

        # initialization of the position of the battleship board to be false
        if orientation == VERTICAL:
            for i in range(0, number_of_positions):
                row = chr(ord(start_position[ROW_IDX]) + i)
                self.positions[(row, start_position[COL_IDX])] = self.sunk
        elif orientation == HORIZONTAL:
            for i in range(0, number_of_positions):
                col = start_position[COL_IDX] + i
                self.positions[(start_position[ROW_IDX], col)] = self.sunk


class Game:
    ########## DO NOT EDIT #########

    _ship_types = ["carrier", "battleship", "cruiser", "submarine", "destroyer"]

    def __init__(self, max_misses=MAX_MISSES):
        """ Creates a new game with max_misses possible missed guesses.
        The board is initialized in this function and ships are randomly
        placed on the board.

        :param max_misses: maximum number of misses allowed before game ends
        """
        self.max_misses = max_misses
        self.ships = []
        self.guesses = []
        self.board = {}
        self.initialize_board()
        self.create_and_place_ships()

    def initialize_board(self):
        """Sets the board to its initial state with each position occupied by
        a period ('.') string.

        :return: None
        """
        range_start = ord(MIN_ROW_LABEL)
        range_end = ord(MAX_ROW_LABEL)
        for row in range(range_start, range_end + 1):
            self.board[chr(row)] = [BLANK_CHAR] * NUM_COLS

    def in_bounds(self, start_position, ship_size, orientation):
        """Checks that a ship requiring ship_size positions can be placed at start position.

        :param start_position: tuple representing the starting position of ship on the board
        :param ship_size: number of positions needed to place ship
        :param orientation: the orientation of the ship ('v' - vertical, 'h' - horizontal)
        :return status: True if ship placement inside board boundary, False otherwise
        """

        if start_position[COL_IDX] + ship_size > NUM_COLS - 1 and orientation == HORIZONTAL:
            return False
        elif ord(start_position[ROW_IDX]) + ship_size > ord(MAX_ROW_LABEL) and orientation == VERTICAL:
            return False
        else:
            return True

    def overlaps_ship(self, start_position, ship_size, orientation):
        """Checks for overlap between previously placed ships and a potential new ship
        placement requiring ship_size positions beginning at start_position in the
        given orientation.

        :param start_position: tuple representing the starting position of ship on the board
        :param ship_size: number of positions needed to place ship
        :param orientation: the orientation of the ship ('v' - vertical, 'h' - horizontal)
        :return status: True if ship placement overlaps previously placed ship, False otherwise
        """

        if orientation == HORIZONTAL:
            rng = range(start_position[COL_IDX], start_position[COL_IDX] + ship_size)
        else:
            rng = range(ord(start_position[ROW_IDX]), ord(start_position[ROW_IDX]) + ship_size)

        for coord in rng:
            if orientation == VERTICAL:
                test = (chr(coord), start_position[COL_IDX])
            else:
                test = (start_position[ROW_IDX], coord)
            for ship in self.ships:
                if test in ship.positions:
                    return True
            return False

    def place_ship(self, start_position, ship_size):
        """Determines if placement is possible for ship requiring ship_size positions placed at
        start_position. Returns the orientation where placement is possible or None if no placement
        in either orientation is possible.

        :param start_position: tuple representing the starting position of ship on the board
        :param ship_size: number of positions needed to place ship
        :return orientation: 'h' if horizontal placement possible, 'v' if vertical placement possible,
            None if no placement possible
        """

        if self.in_bounds(start_position, ship_size, HORIZONTAL) and not self.overlaps_ship(start_position, ship_size,
                                                                                            HORIZONTAL):
            return HORIZONTAL
        elif self.in_bounds(start_position, ship_size, VERTICAL) and not self.overlaps_ship(start_position, ship_size,
                                                                                            VERTICAL):
            return VERTICAL
        else:
            return None

    def create_and_place_ships(self):
        """Instantiates ship objects with valid board placements.

        :return: None
        """
        start_position = get_random_position()

        for ship in self._ship_types:
            orientation = self.place_ship(start_position, SHIP_SIZES[ship])
            while orientation is None:
                start_position = get_random_position()
                orientation = self.place_ship(start_position, SHIP_SIZES[ship])
                break
            self.ships.append(Ship(ship, start_position, orientation))

    def get_guess(self):
        """Prompts the user for a row and column to attack. The
        return value is a board position in (row, column) format

        :return position: a board position as a (row, column) tuple
        """
        row_input = " "
        col_input = -1
        row_range = (ord(MIN_ROW_LABEL), ord(MAX_ROW_LABEL))
        while (MIN_ROW_LABEL > row_input or row_input > MAX_ROW_LABEL) and isinstance(row_input, str):
            row_input = input("Enter a row: ")


        while col_input not in range(NUM_COLS) and isinstance(col_input, int):
            col_input = int(input("Enter a column: "))


        return row_input, col_input

    def check_guess(self, position):
        """Checks whether or not position is occupied by a ship. A hit is
        registered when position occupied by a ship and position not hit
        previously. A miss occurs otherwise.

        :param position: a (row,column) tuple guessed by user
        :return: guess_status: True when guess results in hit, False when guess results in miss
        """
        hit = True
        for ship in self.ships:
            if position in ship.positions and ship.positions[position] == False:
                ship.positions[position] = True
                for pos in ship.positions:
                    if pos == False:
                        hit = False
                if hit == True:
                    print("You sunk the {}!".format(ship.name))
                    ship.sunk = True
                return True
        return False

    def update_game(self, guess_status, position):
        """Updates the game by modifying the board with a hit or miss
        symbol based on guess_status of position.

        :param guess_status: True when position is a hit, False otherwise
        :param position:  a (row,column) tuple guessed by user
        :return: None
        """
        if guess_status:
            self.board[position[ROW_IDX]][position[COL_IDX]] = HIT_CHAR
        else:
            self.guesses.append(position)
            if self.board[position[ROW_IDX]][position[COL_IDX]] == BLANK_CHAR:
                self.board[position[ROW_IDX]][position[COL_IDX]] = MISS_CHAR

    def is_complete(self):
        """Checks to see if a Battleship game has ended. Returns True when the game is complete
        with a message indicating whether the game ended due to successfully sinking all ships
        or reaching the maximum number of guesses. Returns False when the game is not
        complete.

        :return: True on game completion, False otherwise
        """

        count = 0
        for ship in self.ships:
            if ship.sunk == True:
                count += 1
        if count == len(self.ships):
            print("YOU WIN!")
            return True
        elif len(self.guesses) == MAX_MISSES:
            print("SORRY! NO GUESSES LEFT.")
            return True
        else:
            return False

    def display_board(self):
        """ Displays the current state of the board."""

        print()
        print("  " + ' '.join('{}'.format(i) for i in range(len(self.board))))
        for row_label in self.board.keys():
            print('{} '.format(row_label) + ' '.join(self.board[row_label]))
        print()

    ########## DO NOT EDIT #########


def end_program():
    """Prompts the user with "Play again (Y/N)?" The question is repeated
    until the user enters a valid response (Y/y/N/n). The function returns
    False if the user enters 'Y' or 'y' and returns True if the user enters
    'N' or 'n'.

    :return response: boolean indicating whether to end the program
    """

    another_round = input("Play again (Y/N)? ")
    while another_round not in ["N", "n", "Y", "y"]:
        another_round = input("Play again (Y/N)? ")
    if another_round in ["Y", "y"]:
        return False
    if another_round in ["N", "n"]:
        return True


def main():
    """Executes one or more games of Battleship."""

    play_battleship()


if __name__ == "__main__":
    main()