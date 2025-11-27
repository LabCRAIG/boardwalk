from boardwalk import Game, Board, is_movement, is_placement, get_move_elements
from random import choice
import re

class Mastermind(Game):
    
    def __init__(self, board):
        super().__init__(board)
        self.secret = ''.join([choice('ABCD') for _ in range(4)])
        self.max_rounds = board.height
        
    def validate_move(self, move):
        return bool(re.fullmatch(r'[ABCD]{4}', move))
    
    def perform_move(self, move):
        for i, c in enumerate(move):
            self.board.place_piece(f'{c} {self.round}, {i+1}')
            
        # verification
        counts = {c: self.secret.count(c) for c in 'ABCD'}
        
        for i in range(4):
            c = move[i]        
            if c == self.secret[i]:
                self.board.place_piece(f'Y {self.round}, {i+6}')
                counts[c] -= 1
                
            elif c in self.secret and counts[c] > 0:
                self.board.place_piece(f'E {self.round}, {i+6}')
                counts[c] -= 1
                
            else:
                self.board.place_piece(f'N {self.round}, {i+6}')
            
    def game_finished(self):
        return self.round >= self.max_rounds or self.get_winner()
        
    def get_winner(self):
        return 1 if ''.join(self.board.layout[self.round-1][0:4]) == self.secret else None
    
    def next_player(self):
        return self.current_player
    
    def finish_message(self, winner):
        if winner:
            print('You won!')
        else:
            print('You lose')

    
b = Board((6,9), ('____ ____\n'*6)[:-1])
mygame = Mastermind(b)
mygame.game_loop()
