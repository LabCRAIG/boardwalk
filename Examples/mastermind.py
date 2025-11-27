# Mastermind
# The player has 6 chances to guess a randomly chosen 4-letter sequence
# That is any arrangement of the letters ABCDEF
# Guesses are made by directly inputting the guessed 4 letter sequence, e.g. 'BADF'
# The guess will appear on the left column group. The right column group shows how good the guess was
# Each column on the rigth group scores the respective column on the left group
# - Y means a correct letter in the correct position
# - E means a correct letter in an incorrect position
# - N means the letter does not appear in the sequence, or all instances of that letter which do have already been scored

from boardwalk import Game, Board, is_movement, is_placement, get_move_elements
from random import choice
import re

class Mastermind(Game):
    
    def __init__(self, board):
        super().__init__(board)
        self.secret = ''.join([choice('ABCDEF') for _ in range(4)])
        self.max_turns = board.height
        
    def validate_move(self, move):
        return bool(re.fullmatch(r'[ABCDEF]{4}', move))
    
    def perform_move(self, move):
        for i, c in enumerate(move):
            self.board.place_piece(f'{c} {self.turn-1}, {i}')
            
        # verification
        counts = {c: self.secret.count(c) for c in 'ABCDEF'}
        
        # Checks correct position
        for i in range(4):
            c = move[i]        
            if c == self.secret[i]:
                self.board.place_piece(f'Y {self.turn-1}, {i+5}')
                counts[c] -= 1
        # Checks correct letter, wrong position
        for i in range(4):
            c = move[i]
            if c == self.secret[i]:
                continue

            if c in self.secret and counts[c] > 0:
                self.board.place_piece(f'E {self.turn-1}, {i+5}')
                counts[c] -= 1
                
            else:
                self.board.place_piece(f'N {self.turn-1}, {i+5}')
            
    def game_finished(self):
        return self.turn >= self.max_turns or self.get_winner()
        
    def get_winner(self):
        return 1 if ''.join(self.board.layout[self.turn-1][0:4]) == self.secret else None
    
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
