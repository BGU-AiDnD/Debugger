__author__ = 'amir'


import random, Queue
from math import sqrt, log
from random import sample

class Node(object):

    COLORS = {
        1: 'red',
        2: 'yellow',
        3: 'orange',
        4: 'green',
        5: 'blue',
        6: 'purple'
    }

    def __init__(self, parent, action, state, player, game=None):
        if parent is None and game is None:
            raise Exception('No game provided')
        # Game
        self.game = game or parent.game
        # Structure
        self.parent    = parent
        self.children  = dict.fromkeys(self.game.actions(state))
        # Tree data
        self.action    = action
        self.state     = state
        # Search meta data
        self.player    = player
        self.visits    = 0
        self.value     = 0.0

    def __iter__(self):
        """
        A generator function. Does a pre-order traversal over the nodes
        in the tree without using recursion.
        """
        active = Queue.Queue()
        active.put(self)
        while active.qsize() > 0:
            next = active.get()
            for _, child in next.children.items():
                if child is not None:
                    active.put(child)
            yield next

    def __len__(self):
        """
        Returns the number of nodes in the tree. This requires a
        traversal, so it has O(n) running time.
        """
        n = 0
        for node in self.traverse():
            n += 1
        return n

    @property
    def weight(self):
        """
        The weight of the current node.
        """
        if self.visits == 0:
            return 0
        return self.value / float(self.visits)

    def search_weight(self, c):
        """
        Compute the UCT search weight function for this node. Defined as:

            w = Q(v') / N(v') + c * sqrt(2 * ln(N(v)) / N(v'))

        Where v' is the current node and v is the parent of the current node,
        and Q(x) is the total value of node x and N(x) is the number of visits
        to node x.
        """
        return self.weight + c * sqrt(2 * log(self.parent.visits) / self.visits)

    def actions(self):
        """
        The valid actions for the current node state.
        """
        return self.game.actions(self.state)

    def result(self, action):
        """
        The state resulting from the given action taken on the current node
        state by the node player.
        """
        return self.game.result(self.state, action, self.player)

    def terminal(self):
        """
        Whether the current node state is terminal.
        """
        return self.game.terminal(self.state)

    def next_player(self):
        """
        Returns the next game player given the current node's player.
        """
        return self.game.next_player(self.player)

    def outcome(self, player=None):
        """
        Returns the game outcome for the given player (default is the node's
        player) for the node state.
        """
        p = player or self.player
        return self.game.outcome(self.state, p)

    def fully_expanded(self):
        """
        Whether all child nodes have been expanded (instantiated). Essentially
        this just checks to see if any of its children are set to None.
        """
        return not None in self.children.values()

    def expand(self):
        """
        Instantiates one of the unexpanded children (if there are any,
        otherwise raises an exception) and returns it.
        """
        try:
            action = self.children.keys()[self.children.values().index(None)]
        except ValueError:
            raise Exception('Node is already fully expanded')

        state = self.game.result(self.state, action, self.player)
        player = self.game.next_player(self.player)

        child = Node(self, action, state, player)
        self.children[action] = child
        return child

    def best_child(self, c=1/sqrt(2)):
        if not self.fully_expanded():
            raise Exception('Node is not fully expanded')

        return max(self.children.values(), key=lambda x: x.search_weight(c))

    def best_action(self, c=1/sqrt(2)):
        """
        Returns the action needed to reach the best child from the current
        node.
        """
        return self.best_child(c).action

    def max_child(self):
        """
        Returns the child with the highest value.
        """
        return max(self.children.values(), key=lambda x: x.weight)

    def simulation(self, player):
        """
        Simulates the game to completion, choosing moves in a uniformly random
        manner. The outcome of the simulation is returns as the state value for
        the given player.
        """
        st = self.state
        pl = self.player
        while not self.game.terminal(st):
            action = sample(self.game.actions(st), 1)[0]
            st = self.game.result(st, action, pl)
            pl = self.game.next_player(pl)
        return self.game.outcome(st, player)

    def dot_string(self, value=False, prettify=lambda x: x):
        """
        Returns the tree rooted at the current node as a string
        in dot format. Each node is labeled with its state, which
        is first run through prettify. If value is True, then
        the value is included in the node label.
        """
        output = ''
        output += 'digraph {\n'
        for node in self:
            # Define the node
            name = prettify(node.state)
            if value:
                name += '%s\\n' % node.value
            color = self.COLORS[node.player]
            output += '\t"%s" [style="filled", fillcolor="%s"]\n' % (
                name, color
            )
            # No edge into the root node
            if node.parent is None:
                continue
            # Add edge from node parent to node
            pname = prettify(node.parent.state)
            if value:
                pname += '%s\\n' % node.parent.value
            output += '\t"%s" -> "%s"\n' % (pname, name)
        output += '}'
        return output

