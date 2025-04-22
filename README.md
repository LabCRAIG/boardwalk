# Boardwalk

## Purpose

This is a Python package intended to be used for creating board games.

It is composed of two classes: `Board` and `Game`. These classes define, either partially or totally, all the functionalities necessary to program a game's rules and a text-based user interface for the game.

The platform allows for the creation of any game set in a finite, orthogonal board, with any variety of pieces (which can be either placed on the board or moved around the board at will, according to the rules), played by any number of players.

This documentation follows a top-down structure, starting with the higher level `Game` class, which is responsible for the turn-to-turn workings of the game; then the `Board` class, which is responsible for storing the layout of the pieces in play and verifying placement/movement rules. We also explain the expected format for player input and how to handle it.

Whenever the term "user" is used in this documentation, it refers to the programmer who implements their own game with the help of this package.

## Output code format

The expected code defining a game based on this documentation follows the format:

```python
from game import Game, Board, is_movement, is_placement, get_move_elements
<additional imports>

# Game subclass definition
class GameName(Game):
    ...

if __name__ == '__main__':
    board = Board(<arguments>)
    mygame = GameName(<arguments>)
    mygame.game_loop()
```

## Classes

The following is the documentation for the [`Game`](#game) and [`Board`](#board) classes.

### Game

The `Game` class is responsible for handling user interaction and managing the game rules at a high level. It implements methods for verifying and resolving player moves, checking for win conditions, and calculating the turn order of players.

The class also stores the game state, which is a data structure composed of the current board layout, currently active player, and a list of any additional variables necessary to determine the winning condition, player turn order, and potential side effects of future moves.

The `Game` class itself should not be used in your implementation. Rather, you should create a child class of `Game` which overrides all the necessary methods, to enforce the specific rules of your game.

This documentation splits the `Game` class's methods into three categories:

* **Final methods**, which must not be overridden. Customization of the class must be implemented in the class's other methods, which will then be called by the final methods.
* **Optionally overridable methods**, whose default implementations are sufficient for a number of games, but may need to be expanded upon for certain rulesets.
* **Overridable methods**, which must obligatorily be implemented to define the rules of the intended game.

#### Game Attributes

By default, the `Game` class only has three attributes:

* `board`, an object of class `Board` which will store the pieces in play and their placements. This should only ever reference the same object through the entire game's duration, though the state of the board will be modified by several methods, as detailed further below.
* `round`, an integer which stores the current round of the game, beginning at 1. This will be updated within the game loop by the `round_counter` method.
* `current_player`, an identifier of the next player to make a move. This will be updated within the game loop by the `next_player` method. It is best practice to define an enum within your subclass to represent the players as integers, and the `next_player` and `get_winner` methods will be assumed to return integers in this documentation.

These are all initialized within the class constructor. Additional variables, such as flags or counters, might be necessary to define your game states and game-specific rules. These are handled by the user when implementing the subclass.

#### Final methods

`game_loop(self)`: This method is responsible for executing the game until its conclusion, at every turn printing the board in its current state and prompting the active player to make their move.

Below is the code for the method, to illustrate the contexts in which the other methods are called and what values are passed as parameters to each method.

```python
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
```

#### Optionally overridable methods

`__init__(self, board : Board)`: The constructor method.

Default behavior: it receives the `Board` object that will be assigned to the `board` attribute. It sets the `round` attribute to 1, and calls the `initial_player` method to assign an initial value to the `current_player` attribute.

Override cases: when necessary to instantiate any additional attributes, perhaps ones passed as parameters.

---

`prompt_current_player(self) -> str`: Prompts the player to input a move and returns their input.

Default behavior: it's a simple call of the standard Python `input` function with the prompt `"Your move: "`

Override cases: when you wish to provide a personalized prompt string (such as one that informs the current player), or when you want to preprocess the returned string. In case of override, the `super` method will probably not be used.

Preprocessing the move and allowing for more flexible player input requires an understanding of standard move formatting, as defined in [the appendix](#appendix-moves).

---

`get_state(self) -> tuple`: Returns the current game state.

The game state is a data structure ideally represented as a tuple. This tuple has three items:

* Board layout: the layout matrix of the `board` attribute. This is a numpy array of strings, as detailed in the `Board` class. For the sake of code security, return a `deepcopy` of `self.board.layout` rather than a pointer to the actual `layout` attribute.
* Current player: the `current_player` attribute (of a type defined by the user, see the Attributes section above).
* Additional parameters: a list of variables containing user-defined attributes, any deemed necessary to define a unique state.

Default behavior: returns a tuple with the parameters, with the third element being an empty list.

Override cases: when there are any additional variables necessary to differentiate a state. It is recommended to simply modify the list in the tuple returned by the `super` method.

---

`perform_move(self, move : str)`: Updates the board according to the move performed. Also updates any other state variables affected by the move.

Default behavior: assumes a game with no effects resulting from a move other than placing/moving the played piece. Calls the appropriate `Board` method between `place_piece` or `move_piece`.

Override cases: two different situations, which may apply simultaneously:

* The move directly affects the pieces on the board in other ways than simply reallocating the played piece, such as by modifying other pieces (e.g. captures in Othello) or the played piece itself (e.g. promotions in Chess).
* The move changes game state variables such as counters or flags.

It is recommended to call upon the `super` method at the beginning of your own implementation, and you might in fact wish to use it to resolve other effects on the boards. This requires an understanding of standard move formatting, as defined in [the appendix](#appendix-moves).

---

`finish_message(self, winner)`: Prints a message at the conclusion of the game, informing the winner and/or any other information deemed relevant. `winner` is the value returned by the `get_winner` method.

Default behavior: prints the message "Player {winner} wins!".

Override cases: whenever you wish to give a more detailed end of game message. In case of override, the `super` method will probably not be used.

---

`round_counter(self) -> int`: Returns the new value of the `round` attribute after a move has been performed.

Default behavior: simply returns the current `round` value increased by 1.

Override cases: games with non-trivial round calculations. For example, if you wish to allow the same player to make multiple moves within the same turn. Remember to also handle this in your `next_player` method.

---

`initial_player(self) -> int`: Returns the enum value of the first player to act.

Default behavior: returns 0.

Override cases: when you're using non-integer player values or you wish to perform a more specialized first player assignment (e.g. at random).

#### Overridable methods

`validate_move(self, move : str) -> bool`: Verifies whether the informed move is valid.

Your implementation should use your game's rules to verify whether or not specified move is valid to be performed according to the current game state. Return `True` if the move is allowed, `False` otherwise.

This method has a default implementation which checks if the coordinates given in standard move format correspond to real positions on the board (i.e. if there are no index errors). We recommend using it at the beginning of your implementation to simplify it. An example is given below:

``` python
def validate_move(self, move):
    if not super().validate_move(move):
        return False

    # Your implementation
```

It is best practice that this method assumes the received move is properly formatted, having been preprocessed by `prompt_current_player`.

For more detailed informations on how moves are properly formatted, consult [the appendix](#appendix-moves).

---

`game_finished(self) -> bool`: Informs whether or not the game has finished, either because a player has won or because no more moves can be taken. Returns `True` if the game has ended, `False` otherwise.

---

`get_winner(self) -> int`: Evaluates which player (if any) has won the game, returning their enum value. If the game was a draw, return `None`.

---

`next_player(self) -> int`: Returns the enum value of the next player to make a move.

### Board

The `Board` class implements the board the game is played in, i.e. the spaces pieces can occupy and the pieces currently in play. It implements methods for placing/moving pieces.

The `Board` class can be used as-is, without the need to create a subclass. All it requires are the arguments defining its shape and initial layout.

#### Board Attributes

`layout`, a 2D numpy array of single-character strings. This is the board proper. This matrix represents all the spaces on the board and the pieces currently on it, with each type of space and piece being represented by a different character.

`height` and `width`, integers that represent the total height and width of the board (the exact values passed to the constructor).

There are two reserved characters for spaces:

* The underscore `'_'` is the `BLANK` space, which represents a vacant space a piece can occupy.
* The whitespace `' '` is the `NULL` space, which represents a space which no piece can occupy.

By default, a board is initialized with all blank spaces.

#### Methods

As the `Board` class is expected to be used as-is, all methods are considered final.

`__init__(self, shape : tuple[int], layout : str = None)`: The constructor method.

`shape` is a tuple of two integers, which define, respectively, the height and width of the board.

`layout` is an optional string that defines the initial setup of the board, as well boards with unusual (non-rectangular) shapes (which can be represented using null spaces). If this parameter is left blank, the board will be initialized with all blank spaces.

The `layout` must match the `shape`. For a shape `h, w`, the layout must be composed of `h` lines, each `w` character long. The lines must be separated by linebreak characters `\n`. Note that there must not be whitespace between the characters of the layout, except where intended as null spaces.

---

`place_piece(self, move : str)`: Performs the placement action specified by the `move` parameter. The specified piece is placed on the board at the speficied position, replacing whatever character was at that position beforehand.

See [the appendix](#appendix-moves) for how moves are specified.

---

`move_piece(self, move : str)`: Performs the movement action specified by the `move` parameter. The piece at the origin position is moved to the destination position, replacing whatever character was originally at the latter. The destination position is left blank.

See [the appendix](#appendix-moves) for how moves are specified.

**Notice:** This method will always place a `BLANK` space at the origin position. If the user wishes to leave another space or piece at the origin instead, this should be treated within the `perform_move` method in the `Game` subclass. The recommended way is to follow up the `move_piece` method with a call of the `place_piece` method, passing as parameter a move with the intended character to be left behind and the origin position coordinates.

## Appendix: Moves

Moves are one of the central elements for defining the logic of your game, as they are the means through which the game state changes. As such, it is necessary to encode them in a way that is both meaningful and easy to parse.

For the purposes of this platform, we consider that there are two types of moves: _placement_ and _movement_.

Placement represents adding a piece to the board that was not there previously (playing it from the player's "hand", as it were).

Movement represents taking a piece already on the board and moving it to a different space on the board.

These two actions require different informations to be properly executed. A placement needs to specify what kind of piece is being placed, and where. A movement needs to specify the space the piece originally occupied, and the space it is being moved to (what type the piece itself is can be inferred from its original position).

As such, we present below what is called the _standard move representation_:

* Placement: `"X D,D"`, where X is the char that represents a piece and D are integers (of any size). The pair of coordinates represents where the piece will be placed.
* Movement: `"D,D D,D"`, where D are integers (of any size). The first pair of coordinates represents the origin (where the piece originally is), and the second pair represents the destination.

Three functions are implemented to help handling moves:

`is_placement(move : str) -> bool`: Returns `True` if the informed move matches the **placement** action formatting, `False` otherwise.

---

`is_movement(move : str) -> bool`: Returns `True` if the informed move matches the **movement** action formatting, `False` otherwise.

---

`get_move_elements(move: str) -> tuple[str, tuple[int, int]] | tuple[tuple[int, int], tuple[int, int]]`: Returns the relevant elements of the `move` string, separated and converted to their most useful formats.

* If the move is a **placement**, it returns a tuple containing the played piece as a single-character string, and the position it was played to as a tuple of integers.
* If the move is a **movement**, it returns a tuple containing the two positions informed (the origin and the destination), both as tuples of integers.
