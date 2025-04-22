import re
import numpy as np
from copy import deepcopy
from enum import Enum
from math import log10

class Game():
    def __init__(self, board):
        self.board = board
        self.round = 1
        self.current_player = self.initial_player()

    #Final
    def game_loop(self):
        while True:
            print(self.board)
            
            valid = False
            while not valid:
                move = self.prompt_current_player()
                valid = self.validate_move(move)

            self.perform_move(move)

            if self.game_finished():
                print(f'\n{self.board}')
                winner = self.get_winner()
                self.finish_message(winner)
                return winner

            self.current_player = self.next_player()
            self.round = self.round_counter()

    # Optionally overridable 
    def prompt_current_player(self):
        return input("Your move: ")
    
    def get_state(self):
        return (deepcopy(self.board.layout), self.current_player)
    
    def perform_move(self, move):
        if is_placement(move):
            self.board.place_piece(move)
        else:
            self.board.move_piece(move)
    
    def finish_message(self, winner):
        if winner is None:
            print("Game over. It's a tie!")
        else:
            print(f'Player {winner} wins!')
    
    def round_counter(self):
        return self.round + 1
    
    def initial_player(self):
        return 0
    
    # Overridable
    def validate_move(self, move):
        # Checks for standard formatting
        if not any([is_placement(move), is_movement(move)]):
            print('This move is incorrectly formatted. Try again.')
            return False
        
        positions = filter(lambda x: not isinstance(x, str), get_move_elements(move))

        for (x,y) in positions:
            try:
                _ = self.board.layout[x, y]
            
            except IndexError:
                print(f'The position {(x,y)} is not on the board. Try again.')
                return False
            
        return True

    def game_finished(self):
        pass

    def get_winner(self):
        pass

    def next_player(self):
        pass

# Move functions
def is_placement(move : str) -> bool:
    return bool(re.fullmatch(r'.\s+\d+\s*,\s*\d+', move))

def is_movement(move : str) -> bool:
    return bool(re.fullmatch(r'\d+\s*,\s*\d+\s+\d+\s*,\s*\d+', move))

def get_move_elements(move: str) -> tuple[str, tuple[int, int]] | tuple[tuple[int, int], tuple[int, int]]:
    if is_placement(move):
        move = re.sub(r'\s', '', move)
        return move[0], tuple(map(lambda x: int(x), move[1:].split(',')))
    
    if is_movement(move):
        moves = re.findall(r'\d+\s*,\s*\d+', move)
        return tuple([tuple(map(lambda x: int(x), m.split(','))) for m in moves])
    
    return None

class Board():
    BLANK = '_'
    NULL = ' '

    def __init__(self, shape, layout = None):
        self.layout = np.full(shape, self.BLANK)
        self.height, self.width = shape
            
        if layout:
            try:
                for i, row in enumerate(layout.split('\n')):
                    for j, c in enumerate(row):
                        self.layout[i,j] = c

            except IndexError:
                raise ValueError('Board layout does not match specified board shape.')

    def place_piece(self, move):
        piece, (x,y) = get_move_elements(move)
        self.layout[x, y] = piece
        
    def move_piece(self, move):
        (x0, y0), (x1, y1) = get_move_elements(move)
        piece = self.layout[x0,y0]
        self.layout[x0,y0] = self.BLANK
        self.layout[x1,y1] = piece
    
    def __str__(self):
        rows, cols = len(self.layout), len(self.layout[0])

        row_width = int(log10(rows)+1)
        first_spacing = ' '*(row_width + 1)
        col_width = int(log10(cols)) + 1
        col_left = ' '*(col_width//2)
        col_right = ' '*(col_width - (col_width//2))

        header = first_spacing + ' '.join([('{:'+ f'{col_width}' + 'd}').format(i) for i in range(cols)]) + '\n'
        for i in range(rows):
            header += ('{:'+ f'{row_width}' + 'd}').format(i) + ' ' + col_left + col_left.join([f'{self.layout[i,j]}{col_right}' for j in range(cols)]) +'\n'

        return header
    
if __name__ == '__main__':
    pass
    