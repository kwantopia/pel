import random
import argparse

"""
    Run:

    # for playing basic computer
    python tictactoe.py

    # for playing smart computer
    python tictactoe.py --smart
"""

class TicTacToe:

    def __init__(self, smart=None):
        self.board = [" ", " ", " ",
                " ", " ", " ",
                " ", " ", " "]

        self.smart = False
        if smart:
            self.smart = True

    def print_reference(self):
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
                if self.board[cell-1] is " ":
                    self.board[cell-1] = 'O'
                    played = True

    def play_smart_computer(self):
        print "Playing smart"
        played = False
        while not played:
            cell = random.randint(1, 9)
            if self.board[cell-1] is " ":
                self.board[cell-1] = 'O'
                played = True

    def check_winner(self):
        """
        :return True if there is a winner else returns False
        """
        wins = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 4, 8],
            [2, 4, 6],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8]
        ]

        for w in wins:
            if self.board[w[0]] != " " and self.board[w[0]] == self.board[w[1]] and self.board[w[0]] == self.board[w[2]]:
                print "{0} is the winner!".format(self.board[w[0]])
                return True

        # check if tied
        if " " not in self.board:
            # the game must have tied since all cells are filled
            print "The game is a tie!"
            return True

        return False

    def run(self):
        running = True
        while running:
            cmd = raw_input('What is your next move?\n')
            if cmd == 'q':
                running = False
            elif cmd == 'r':
                self.print_reference()
            elif cmd == 's':
                self.print_board()
            elif int(cmd) in range(1, 10):
                cell = int(cmd) - 1
                # place user X in the corresponding cell
                if self.board[cell] is " ":
                    self.board[cell] = 'X'
                    if self.check_winner():
                        break
                    self.play_computer()
                    self.print_board()
                    if self.check_winner():
                        break
                else:
                    print "Cell {0} is already taken\n".format(cmd)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--smart", help="play smart computer", action="store_true")
    args = parser.parse_args()

    if args.smart:
        game = TicTacToe(args.smart)
    else:
        game = TicTacToe()
    game.run()
