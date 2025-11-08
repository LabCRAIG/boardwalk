# Example of implementing a simple game (Tic-Tac-Toe) with Boardwalk, as well as using AI agents.
# This exemplifies the minimal implementation with only four methods.

from boardwalk import Game, Board, is_movement, is_placement, get_move_elements
from random import choice

class TicTacToe(Game):
    # Player enum
    X = 0
    O = 1

    # Auxiliary variable to avoid repeating checks
    # for the winning condition
    winner = None
    
    def validate_move(self, move):
        # Checks that the move is within bounds
        if not super().validate_move(move):
            return False
        
        # Checks that the move is a properly formatted placement move,
        # as that is the only valid type of move
        if not is_placement(move):
            return False
        
        # Gets the piece and position of the move informed
        piece, position = get_move_elements(move)
        x, y = position

        # The player may only play their own piece
        if piece != ['X','O'][self.current_player]:
            return False
        
        # The played position must be blank
        if self.board[x,y] != Board.BLANK:
            return False
        
        return move
    
    def next_player(self):
        # Alternates players
        return TicTacToe.X if self.current_player == TicTacToe.O else TicTacToe.O
    
    def game_finished(self):
        # Checks if the board is full (trivial ending)
        is_full = True
        for i in range(3):
            for j in range(3):
                if self.board[i,j] == Board.BLANK:
                    is_full = False

        if is_full:
            return True
        
        # Checks for winning line
        
        # Horizontals
        for i in range(3):
            if self.board[i,0] == self.board[i,1] == self.board[i,2] != Board.BLANK:
                self.winner = self.board[i,0]
                return True

        # Verticals
        for i in range(3):
            if self.board[0,i] == self.board[1,i] == self.board[2,i] != Board.BLANK:
                self.winner = self.board[0,i]
                return True
            
        # Diagonals
        if self.board[0,0] == self.board[1,1] == self.board[2,2] != Board.BLANK or \
           self.board[0,2] == self.board[1,1] == self.board[2,0] != Board.BLANK:
            self.winner = self.board[1,1]
            return True
        
        return False
    
    def get_winner(self):
        # Returns enum based on the winner identified in game_finished

        # Tie
        if self.winner is None:
            return None
        
        # Winner
        return self.X if self.winner == 'X' else self.O
    
    def possible_moves(self, state):
        n = self.board.width
        piece = 'X' if self.current_player == self.X else 'O'

        return [f'{piece} {i},{j}' for j in range(n) for i in range(n) if self.board[i,j] == Board.BLANK]
    
class RandomAgent(object):
    def get_action(self, game, state):
        actions = game.possible_moves(state)
        return choice(actions)

if __name__ == '__main__':
    board = Board((3,3))
    rand = RandomAgent()
    game = TicTacToe(board, ai_players={1:rand})

    game.game_loop()