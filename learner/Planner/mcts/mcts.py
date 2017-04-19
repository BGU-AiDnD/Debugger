"""
A collection of classes and functions for playing certain types of
games. Specifically, an implementation of the MCTS algorithm.
"""
import InstanceNode
import gc
states={}

def clear_states():
    global states
    states.clear()
    import gc
    gc.collect()

def generateState(parent, action, ei, approach):
    global states
    key = repr(ei)
    if key not in states:
        state = InstanceNode.InstanceNode(parent, action, ei, approach)
        states[key]= state
    return states[key]

def getStateIfExists(parent, action, ei):
    global states
    key = repr(ei)
    if key not in states:
        return None
    states[key].add_parent(parent, action)
    return states[key]

def mcts_uct(ei, iterations, approach):
    """
    Implementation of the UCT variant of the MCTS algorithm.
    """
    clear_states()
    root = generateState(None, None, ei, approach)
    for i in xrange(iterations):
        child = root
        while not child.terminal() and (not child.experimentInstance.AllTestsReached()):
            if not child.fully_expanded():
                child = child.expand()
                break
            else:
                child = child.best_child()
        cost = child.simulation()
        update_parents(child, cost)
    return root.best_action(c=0)

def update_parents(child, cost):
    if child is None:
        return
    for p in child.parents:
        parent = child.parents[p]
        parent.visits[p] += 1
        parent.value[p] += cost
        update_parents(parent, cost)