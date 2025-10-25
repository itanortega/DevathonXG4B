class TicTacToe:
    def __init__(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_turn = "X"
        self.winner = None
        self.game_over = False

    def make_move(self, row, col, player):
        if self.game_over or self.board[row][col] != "":
            return False

        if player != self.current_turn:
            return False

        self.board[row][col] = player

        if self.check_winner(row, col, player):
            self.winner = player
            self.game_over = True
        elif self.is_board_full():
            self.game_over = True

        self.current_turn = "O" if player == "X" else "X"
        return True

    def check_winner(self, row, col, player):
        # Check row
        if all(self.board[row][c] == player for c in range(3)):
            return True
        # Check column
        if all(self.board[r][col] == player for r in range(3)):
            return True
        # Check diagonals
        if row == col and all(self.board[i][i] == player for i in range(3)):
            return True
        if row + col == 2 and all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def is_board_full(self):
        return all(cell != "" for row in self.board for cell in row)

    def get_state(self):
        return {
            "board": self.board,
            "current_turn": self.current_turn,
            "winner": self.winner,
            "game_over": self.game_over
        }