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
        
        num, pos = get_move_elements(move)
        if num == Board.BLANK:
            return len(board[pos]) == 1
        
        try:
            num = int(num)
            return 0 <= num <= 9
        except:
            return False
        
    def game_finished(self):
        if '_' in board:
            return False
        
        n = self.board.width
        numbers = set(range(1,n+1))

        for row in self.board.layout:
            pass
            

    
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
