import random
import argparse

"""
    Run:

    # for playing basic computer
    python tictactoe.py

    # for playing smart computer
    python tictactoe.py --smart
"""

class GameErrorException(Exception):

    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return self.message


class TicTacToe:

    def __init__(self, smart=None):
        self.board = [" ", " ", " ",
                " ", " ", " ",
                " ", " ", " "]

        self.smart = False
        if smart:
            self.smart = True

        # board index for winning
        self.wins = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 4, 8],
            [2, 4, 6],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8]
        ]

        self.winning_sets = [
            set([0, 1, 2]),
            set([3, 4, 5]),
            set([6, 7, 8]),
            set([0, 4, 8]),
            set([2, 4, 6]),
            set([0, 3, 6]),
            set([1, 4, 7]),
            set([2, 5, 8])
        ]

        self.x_positions = set([])
        self.o_positions = set([])


    def print_reference(self):
        """
        Print the reference board cell numbers
        """
        print "1 | 2 | 3"
        print "---------"
        print "4 | 5 | 6"
        print "---------"
        print "7 | 8 | 9"
        print "\n"

    def print_board(self):
        print ""
        for row in range(0, 3):
            col_start = row*3
            print "{0} | {1} | {2}".format(self.board[col_start], self.board[col_start+1], self.board[col_start+2])
            if row < 2:
                print "---------"
            else:
                print ""

    def play_computer(self):
        if self.smart:
            self.play_smart_computer()
        else:
            played = False
            while not played:
                cell = random.randint(1, 9)
                board_index = cell - 1
                if self.board[board_index] is " ":
                    self.board[board_index] = 'O'
                    self.o_positions.add(board_index)
                    played = True

    def play_smart_computer(self):
        #print "** Playing smart"
        """
        1. Pick the center cell 5 (board_index = 4) if not, to increase chances
        2. Block any possible completions by X that is advantageous to O
        3. If have possible winning completion, get it done and win
        """
        played = False
        while not played:
            center_index = 4
            if self.board[center_index] == " ":
                self.board[center_index] = 'O'
                self.o_positions.add(center_index)
                played = True
            else:
                # check X's moves and place O where it's intersection of X's winning positions and O's winning positions
                print "X positions: ", self.x_positions
                x_winning = self.get_winning_positions(self.x_positions)
                print "X winnings: ", x_winning
                print "O positions: ", self.o_positions
                o_winning = self.get_winning_positions(self.o_positions)
                print "O winnings: ", o_winning

                # next move should be intersection of x_winning and o_winning
                possible_win_moves = x_winning.intersection(o_winning)
                print "Possible win moves: ", possible_win_moves
                move_choices_len = len(possible_win_moves)
                if move_choices_len == 1:
                    # there's one good possible win moves
                    board_index = list(possible_win_moves)[0]
                elif move_choices_len > 1:
                    # select random index from possible_win_moves
                    board_index = random.choice(list(possible_win_moves))
                else:
                    if len(x_winning) > 0:
                        # try to block X by placing in cell that X may win
                        board_index = random.choice(list(x_winning))
                    else:
                        # get remaining positions
                        left_over_positions = self.get_remaining_positions()
                        #print "**Left over: ", left_over_positions
                        if len(left_over_positions) > 0:
                            board_index = random.choice(left_over_positions)
                        else:
                            # something is wrong, game is over and all positions are taken
                            raise GameErrorException("No left over positions")
                if self.board[board_index] == " ":
                    self.board[board_index] = 'O'
                    self.o_positions.add(board_index)
                    played = True
                else:
                    print "Computer chose a filled cell position: ", board_index

    def get_winning_positions(self, current_positions):
        """
            Find those cells where one can play advantageous 
        """
        winning_moves = set([])
        for w_set in self.winning_sets:
            print w_set
            if current_positions <= w_set:
                remaining_choices = w_set - current_positions - set(self.get_occupied_positions())
                if len(remaining_choices) == 1:
                    # if there's one winning move left, then just return that one so that it can be blocked
                    winning_moves = remaining_choices
                    return winning_moves
                winning_moves |= remaining_choices

        return winning_moves

    def get_occupied_positions(self):
        return [i for i, elem in enumerate(self.board) if elem != " "]

    def get_remaining_positions(self):
        return [i for i, elem in enumerate(self.board) if elem == " "]

    def check_winner(self):
        """
        :return True if there is a winner else returns False
        """
        for w in self.wins:
            if self.board[w[0]] != " " and self.board[w[0]] == self.board[w[1]] and self.board[w[0]] == self.board[w[2]]:
                print "** {0} is the winner!".format(self.board[w[0]])
                return True

        # check if tied
        if " " not in self.board:
            # the game must have tied since all cells are filled
            print "** The game is a tie!"
            return True

        return False

    def run(self):
        running = True
        while running:
            cmd = raw_input('What is your next move? (r, q or 1..9 for cell number)\n')
            if cmd == 'q':
                running = False
            elif cmd == 'r':
                self.print_reference()
            elif cmd == 's':
                self.print_board()
            elif int(cmd) in range(1, 10):
                board_index = int(cmd) - 1
                # place user X in the corresponding cell
                if self.board[board_index] is " ":
                    self.board[board_index] = 'X'
                    self.x_positions.add(board_index)
                    if self.check_winner():
                        self.print_board()
                        break
                    self.play_computer()
                    if self.check_winner():
                        self.print_board()
                        break
                    self.print_board()
                else:
                    print "** Cell {0} is already taken\n".format(cmd)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--smart", help="play smart computer", action="store_true")
    args = parser.parse_args()

    if args.smart:
        game = TicTacToe(args.smart)
    else:
        game = TicTacToe()
    game.run()
