# Author: Yingtong Deng
# Tic-tac-toe
# Date due: 2020-11-20


MAX_ROUNDS = 9
NUM_ROWS = 3
NUM_COLS = 3
NUM_POSITIONS = 9
ROW_POS = 0
COL_POS = 1


def reset_board(board):
    """Resets the board dict to its original state with each
    position being empty (i.e. the (row, column) key has a
    space character (' ') value).

    :param board: a dict of (row, column) tuple keys and string values
    :return: None
    {(0, 0): ' ', (0, 1): ' ', (0, 2): ' ', (1, 0): ' ', (1, 1): ' ', (1, 2): ' ', (2, 0): ' ', (2, 1): ' ', (2, 2): ' '}
    """
    for key in board:
        board[key] = ' '


def get_current_player(round):
    """Returns the mark of the player whose turn it is in the current
    round of the game.

    :param round: integer value representing the round
    :return: 'X' or 'O' depending on round
    """

    if round % 2 > 0:
        return "O"
    else:
        return "X"


def get_position_choice(board, player_mark):
    """Prompts the user for a valid (row, col) board position. Prompts
    for row and column are repeated until valid position provided. The
    valid (row, col) position chosen is returned.

    :param board: a dict of (row, col) tuple keys and string values
    :param player_mark: 'X' or 'O' depending on round
    :return: (row, col) tuple of integers representing valid position choice
    """
    print(player_mark, ",", sep="")
    valid_num = ("0", "1", "2")
    row = None
    col = None
    occupied = True
    while occupied:
        row = input("Choose your row: ")
        while row not in valid_num:
            row = input("Choose your row: ")
        col = input("Choose your column: ")
        while col not in valid_num:
            col = input("Choose your column: ")
        position = (int(row), int(col))
        occupied = board[position] != " "
        print()
    return position


def update_board(board, player_mark, position):
    """Updates the value at the key represented by position
    in board dictionary to player_mark.

    :param board: a dict of (row, col) tuple keys and string values
    :param player_mark: 'X' or 'O' depending on round
    :param position: (row, col) tuple representing position
    :return: None
    """
    board[position] = player_mark


def display_outcome(round):
    """Displays an outcome message for a completed Tic-tac-toe game.

    :param round: the final value of the round variable for the game
    :return: None
    """
    if round == MAX_ROUNDS:
        print("It's a draw!\n")
    elif round % 2 == 0 and round < MAX_ROUNDS:
        print("X wins!\n")
    elif round % 2 > 0 and round < MAX_ROUNDS:
        print("O wins!\n")


def check_positions(pos1_value, pos2_value, pos3_value):
    """Returns True when all parameters have a value of 'X' or
    all parameters have a value of 'O'. Returns False for all
    other value combinations.

    :param pos1_value: the first of 3 consecutive board position values
    :param pos2_value: the second of 3 consecutive board position values
    :param pos3_value: the third of 3 consecutive board position values
    :return: True when all 3 values are 'X' or when all 3 values are 'O', False otherwise

    """
    (pos_val1, pos_va2, pos_val3) = (pos1_value, pos2_value, pos3_value)
    if (pos_val1, pos_va2, pos_val3) == ('X', 'X', 'X') or (pos_val1, pos_va2, pos_val3) == ('O', 'O', 'O'):
        return True
    else:
        return False


def is_game_complete(board):
    """Determines whether or not a winning configuration has been achieved in the game
    represented by the board. Returns True when a winning configuration is detected and
    False when no winning configuration exists on the board.

    :param board: a dict of (row, col) tuple keys and string values
    :return: True when a winning configuration is detected, False otherwise
    """
    configuration = [
        (board[0, 0], board[0, 1], board[0, 2]),
        (board[1, 0], board[1, 1], board[1, 2]),
        (board[2, 0], board[2, 1], board[2, 2]),
        (board[0, 0], board[1, 0], board[2, 0]),
        (board[0, 1], board[1, 1], board[2, 1]),
        (board[0, 2], board[1, 2], board[2, 2]),
        (board[0, 0], board[1, 1], board[2, 2]),
        (board[0, 2], board[1, 1], board[2, 0]),
    ]

    winning_configuration = False
    index = 0
    while winning_configuration is False and index < len(configuration):
        position_1 = configuration[index][0]
        position_2 = configuration[index][1]
        position_3 = configuration[index][2]
        winning_configuration = check_positions(position_1, position_2, position_3)
        index += 1

    return winning_configuration


def play_tic_tac_toe(board):
    """Controls Tic-tac-toe games. This includes prompting player's for
    position choices, checking for winning game configurations, and outputting
    the outcome of a game.

    :param board: a dict of (row, col) tuple keys and string values
    :return: None
    """
    print("Let's Play Tic-tac-toe!\n")
    status = False
    another_round = False
    while not another_round:
        round = 0
        while status == False and round < MAX_ROUNDS:
            display_board(board)
            player = get_current_player(round)
            position = get_position_choice(board, player)
            update_board(board, player, position)
            status = is_game_complete(board)
            if status == False:
                round += 1
        display_board(board)
        display_outcome(round)
        another_round = is_program_finished()
        if another_round == False:
            reset_board(board)
            status = False
    print("Goodbye.")


def is_program_finished():
    """Prompts the user with the message "Play again (Y/N)?". The question is repeated
    until the user enters a valid response (one of Y/y/N/n). The function
    returns False if the user enters 'Y' or 'y' and returns True if the user
    enters 'N' or 'n'.

    :return response: boolean representing program completion status
    """
    another_round = None
    while another_round not in ("Y", "N", "n", "y"):
        another_round = input("Play again (Y/N)? ")
    print()
    if another_round == "Y" or another_round == "y":
        return False
    elif another_round == "N" or another_round == "n":
        return True


def display_board(board):
    """Displays the board's current state as a 3x3 grid"""

    print("     0 1 2 ")

    for row in range(0, NUM_ROWS):
        print("  {}  ".format(row), end="")
        for col in range(0, NUM_COLS):
            if col == 0:
                print(board[(row, col)], end="")
            else:
                print("|{}".format(board[(row, col)]), end="")

        print(" ")

        if row < NUM_ROWS - 1:
            print("    --+-+--")
    print()


def main():

    board = {
        (0, 0): ' ', (0, 1): ' ', (0, 2): ' ',
        (1, 0): ' ', (1, 1): ' ', (1, 2): ' ',
        (2, 0): ' ', (2, 1): ' ', (2, 2): ' '
    }

    # call play_tic_tac_toe() with board as argument and remove pass below
    play_tic_tac_toe(board)


if __name__ == '__main__':
    main()