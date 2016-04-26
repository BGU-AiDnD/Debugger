__author__ = 'amir'

import Game

class ConnectFour(Game.Game):
    """
    Implementation of the game Connect Four, modeled as a tree search problem.

    The state is a tuple of tuples. The last element is the player whose turn
    it is, the rest of the elements are tuples that represent columns in the
    game board. The first element in each corresponds to the bottom slot in the
    game board. If a slot is not occupied then it simply is not present in the
    state representation.

    ( (), (), (), (), 1 ) Four empty columns, player 1's turn

    An action is just an integer representing a column in the game board
    (state). The player is taken from the state and the move is attributed to
    this player.
    """
    PLAYERS = (1,2)
    HEIGHT = 4
    WIDTH = 4

    TARGET = 3

    VALUE_WIN = 1
    VALUE_LOSE = -1
    VALUE_DRAW = 0

    def __init__(self, players=PLAYERS, height=HEIGHT, width=WIDTH, target=TARGET):
        self.players  = players
        self.height   = height
        self.width    = width
        self.target   = target

    def _legal(self, state, action):
        if action not in xrange(len(state)):
            raise Exception('Invalid action: out of range')
        return len(state[action]) < self.height

    def _streak(self, state, player, start, delta, length=0):
        # Check for out-of-bounds at low end b/c of wrapping
        row, column = start
        if row < 0 or column < 0:
            return False
        try:
            piece = state[column][row]
        except IndexError:
            return False
        if piece != player:
            return False
        # Current slot is owned by the player
        length += 1
        if length == self.target: # Streak is already long enough
            return True
        # Continue searching,
        drow, dcolumn = delta
        return self._streak(
            state,
            player,
            (row + drow, column + dcolumn),
            delta,
            length
        )

    def pretty_state(self, state, escape=False):
        output = ''
        for j in range(self.width):
            output += ' ' + str(j)
        output += ' '
        if escape:
            output += '\\n'
        else:
            output += '\n'
        i = self.height - 1
        while i >= 0:
            for column in state:
                if len(column) > i:
                    output += '|' + str(column[i])
                else:
                    output += '| '
            output += '|'
            if escape:
                output += '\\n'
            else:
                output += '\n'
            i -= 1
        return output

    def actions(self, state):
        return tuple(
            [i for i, _ in enumerate(state) if self._legal(state, i)]
        )

    def result(self, state, action, player):
        if not self._legal(state, action):
            raise Exception('Illegal action')
        newstate = []
        for index, column in enumerate(state):
            if index == action:
                newstate.append(column + (player,))
            else:
                newstate.append(column)
        return tuple(newstate)

    def terminal(self, state):
        # All columns full means we are done
        if all([len(column) == self.height for column in state]):
            return True
        # A winner also means we are done
        if self.outcome(state, self.players[0]) != self.VALUE_DRAW:
            return True
        # Board is not full and no one has won so the game continues
        return False

    def next_player(self, player):
        if player not in self.players:
            raise Exception('Invalid player')
        index = self.players.index(player)
        if index < len(self.players) - 1:
            return self.players[index + 1]
        else:
            return self.players[0]

    def outcome(self, state, player):
        for ci, column in enumerate(state):
            for ri, marker in enumerate(column):
                if any((
                    self._streak(state, marker, (ri, ci), (1, 0)),
                    self._streak(state, marker, (ri, ci), (0, 1)),
                    self._streak(state, marker, (ri, ci), (1, 1)),
                    self._streak(state, marker, (ri, ci), (1, -1)),
                )):
                    # A winner was found
                    if marker == player:
                        return self.VALUE_WIN
                    else:
                        return self.VALUE_LOSE
        # No winner was found
        return self.VALUE_DRAW

