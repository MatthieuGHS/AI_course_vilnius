################################
# STATE SEARCH ALGORITHM - THIN
# (minimum abstraction version)
################################

# PATH
# (solution data type)
#
# Implied to be a list of states and actions connecting them

def path_length (path):
    """ Return number of actions in path. """
    return len(path)//2


def path_states (path):
    """ Return all states in path. """
    return path[0::2]


def path_actions (path):
    """ Return all actions in path. """
    return path[1::2]


# Problem-domain-dependent features

def path_reverse (path):
    """ Reverse path direction. """
    return path[::-1]


def path_result (path):
    """ Return relevant solution form of the path. """
    return path_actions(path)


def path_compare (path, answer):
    """ Compare path to a stored answer. """
    return (path == answer)


# FRONTIER
# (path list data type)
#
# Implied to be either a list or a deque

from collections import deque


# Sorted-insertion functions for queue

def queue_index (queue, path, cost):
    """ Find queue insertion point for path using bisection. """
    cost_path = cost(path)
    # Do trivial checks first,
    #  if your problem results in many first/last insertions
    try:                                                #--#
        if cost_path < cost(queue[0]):      return 0    #--#
    except IndexError:                      return 0    #--#
    lo, hi = 0, len(queue)
    if cost_path >= cost(queue[hi-1]):      return hi   #--#
    # Carry on with bisection
    while lo < hi:
        mid = (lo+hi)//2
        if cost_path < cost(queue[mid]):    hi = mid
        else:                               lo = mid+1
    return lo


def queue_update (queue, path, cost):
    """ Find place and insert item into deque. """
    i = queue_index(queue, path, cost)
    queue.insert(i, path)


# SEARCH
#
# The only purpose of class *here*
#   is to keep track of search depth

class StateSearch:
    """ State-space search implementation class. """

    # Default search depth
    search_depth = 20


    def __init__ (self, depth=None):
        """Initialize search object."""
        self.depth = depth or self.search_depth


    # DEPTH-FIRST SEARCH

    def depth_tree (self, model, loopcheck=True):
        """ Depth-first search without memory. """
        (start, goal, successors, cost) = model
        if goal(start): return [start]
        frontier = [ [start] ]
        while frontier:
            path = frontier.pop()
            if path_length(path) >= self.depth: continue
            state = path[-1]
            for (action, new_state) in successors(state):
                if not loopcheck or new_state not in path:
                    new_path = path + [action, new_state]
                    if goal(new_state): return new_path
                    frontier.append(new_path)
        return []


    def depth_graph (self, model):
        """ Depth-first search with memory. """
        (start, goal, successors, cost) = model
        if goal(start): return [start]
        frontier = [ [start] ]
        explored = { start: 0 }
        while frontier:
            path = frontier.pop(); d = path_length(path)
            if d >= self.depth: continue
            state = path[-1]
            for (action, new_state) in successors(state):
                if new_state not in explored or explored[new_state] > d+1:
                    new_path = path + [action, new_state]
                    if goal(new_state): return new_path
                    frontier.append(new_path)
                    explored[new_state] = d+1
        return []


    # ITERATIVE DEEPENING

    def iterate (self, f, model):
        """ Perform iterative deepening search. """
        depth = self.depth
        for d in range(1, depth+1):
            self.depth = d; result = f(model); self.depth = depth
            if result: return result
        return []


    # BREADTH-FIRST SEARCH

    def breadth (self, model, memory=True):
        """ Breadth-first search. """
        (start, goal, successors, cost) = model
        if goal(start): return [start]
        frontier = deque([ [start] ])
        explored = set([ start ]) if memory else set([ ])
        while frontier:
            path = frontier.popleft()
            if path_length(path) >= self.depth: continue
            state = path[-1]
            for (action, new_state) in successors(state):
                known = (path if memory == False else explored)
                if new_state not in known:
                    new_path = path + [action, new_state]
                    if goal(new_state): return new_path
                    frontier.append(new_path)
                    if memory: explored.add(new_state)
        return []


    # COST-BASED SEARCH

    def mcost (self, model, memory=True):
        """ Minimal-cost search. """
        (start, goal, successors, cost) = model
        if not cost: cost = path_length
        if goal(start): return [start]
        frontier = deque([ [start] ])
        explored = set([ ])
        leaves = { start: [start] }
        while frontier:
            path = frontier.popleft()
            state = path[-1]
            leaves.pop(state)
            if goal(state): return path
            if memory: explored.add(state)
            if path_length(path) >= self.depth: continue
            for (action, new_state) in successors(state):
                known = (path if memory == False else explored)
                if new_state not in known:
                    new_path = path + [action, new_state]
                    curr = leaves.get(new_state, None)
                    if curr:
                        if cost(new_path) < cost(curr):
                            frontier.remove(curr)
                        else: continue
                    queue_update(frontier, new_path, cost)
                    leaves[new_state] = new_path
        return []


    # SEARCH STRATEGIES BY NAME
    #
    # Best versions are automatically selected

    def dfts (self, model):
        return self.depth_tree (model, loopcheck=False)


    def dfps (self, model):
        return self.depth_tree (model, loopcheck=True)


    def dfgs (self, model):
        return self.depth_graph (model)


    dftq = dfts
    dfpq = dfps
    dfgq = dfgs


    def idts (self, model):
        return self.iterate (self.dfts, model)


    def idps (self, model):
        return self.iterate (self.dfps, model)


    def idgs (self, model):
        return self.iterate (self.dfgs, model)


    idtq = idts
    idpq = idps
    idgq = idgs


    def bftq (self, model):
        return self.breadth (model, memory=None)


    def bfpq (self, model):
        return self.breadth (model, memory=False)


    def bfgq (self, model):
        return self.breadth (model, memory=True)


    bfts = bftq
    bfps = bfpq
    bfgs = bfgq


    def lctq (self, model):
        return self.mcost (model, memory=None)


    def lcpq (self, model):
        return self.mcost (model, memory=False)


    def lcgq (self, model):
        return self.mcost (model, memory=True)


    lcts = lctq
    lcps = lcpq
    lcgs = lcgq
    mcts = lctq
    mcps = lcpq
    mcgs = lcgq
    mctq = lctq
    mcpq = lcpq
    mcgq = lcgq

