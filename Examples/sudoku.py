# 6x6 Sudoku
# Letters are used instead of numbers to allow better visualization
# Uppercase letters are fixed on the board, while players place 
# lowercase letters.

from boardwalk import Game, Board, is_movement, is_placement, get_move_elements

class Sudoku(Game):
    def __init__(self, board: Board, ai_players={}):
        super().__init__(board, ai_players)

        self.box_width = 3
        self.box_height = 2
        self.boxes_per_row = 2
        self.boxes_per_col = 3

    def validate_move(self, move):
        if not super().validate_move(move):
            return False
        
        if not is_placement(move):
            return False
        
        c, pos = get_move_elements(move)
        if board[pos] in 'ABCDEF':
            return False
        
        return c.lower() in 'abcdef'
        
    def game_finished(self):
        if '_' in board:
            return False
        
        n = self.board.width
        letters = {c for c in 'abcdef'}

        for row in self.board.layout:
            row = [c.lower() for c in row]
            if set(row) != letters:
                return False
        return True
    
    
    def get_winner(self):
        return 0
    
    def next_player(self):
        return 0

s= """\
___F__
DF__EC
ABC___
____CA
BE__AD
CADE_F"""


board = Board((6,6), s)
game = Sudoku(board)

game.game_loop()
