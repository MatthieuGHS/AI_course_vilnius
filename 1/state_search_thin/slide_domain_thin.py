####################################
# SLIDE PUZZLE SEARCH DOMAIN - THIN
# (minimum abstraction version)
####################################

# STATE  is row-major one-dimensional tuple of tile numbers
# ACTION is the direction of moving the EMPTY slide
# ANSWER is an array of actions (moves)


# Global constants

SPACE = 0 # Empty tile designation
SIZE  = 4 # Default puzzle size


# Problem-domain-dependent path features

def path_actions (path):
    """ Return all actions in path. """
    return path[1::2]


def path_reverse (path):
    """ Reverse path direction. """
    flip = { 'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L' }
    reverse = path[::-1]
    for i in range(1, len(reverse), 2):
        reverse[i] = flip[reverse[i]]
    return reverse


def path_solved (path):
    """ Return relevant solution form of the path. """
    return path_actions(path)


def path_compare (path, answer):
    """ Compare path to a stored answer. """
    return tuple(path_solved(path)) == tuple(answer)


# Helper functions

def tile_swap (T, i, j):
    """ Swap two elements in a tuple. """
    return T[:i] + (T[j],) + T[i+1:j] + (T[i],) + T[j+1:]


def create_goal (size=SIZE, first=True):
    """ Create ordered tuple with space as first or last element. """
    if first: return (SPACE,) + tuple(range(1,size*size))
    else:     return tuple(range(1,size*size)) + (SPACE,)


def print_state (state, N):
    """ Print current state. """
    for (i, tile) in enumerate(state):
        print (('%2d' % tile)
               if tile != SPACE else
               ('%2s' %  ' ')
               , end=' ')
        if (i+1)%N != 0:    print ('|', end=' ')
        elif i+1 < N*N:     print ('\n' + (N*N+1)*'-')
    print()


# SEARCH DOMAIN

class SlideDomain:
    """ Slide puzzle domain definition class. """

    def __init__ (self, start, size=SIZE, first=True, answer=None):
        """ Set up slide puzzle. """
        self.size = size                        # Puzzle size
        self.goal = create_goal(size, first)    # Form of goal state
        self.start = start                      # Start state (a tuple!)
        self.answer = answer                    # Stored solution


    def show (self):
        """ Print current puzzle. """
        print_state(self.start, self.size)


    def is_goal (self, state):
        """ Goal check function for slide puzzle. """
        return state == self.goal


    def go_next (self, state):
        """ Successor function for slide puzzle. """
        succ = {}
        i, N = state.index(SPACE), self.size
        if i%N != 0:
            succ['L'] = tile_swap(state,i-1,i)
        if (i+1)%N != 0:
            succ['R'] = tile_swap(state,i,i+1)
        if i>=N:
            succ['U'] = tile_swap(state,i-N,i)
        if i<(N-1)*N:
            succ['D'] = tile_swap(state,i,i+N)
        return succ.items()


    def astar_cost (self, path):
        """ A* cost function for slide puzzle. """
# ===
# HW: implement A* cost function
# ===
        return 0


# EXAMPLE PROBLEMS

M = SIZE
puzzle0 = SlideDomain(tuple(range(1,M)) + (0,) + tuple(range(M,M*M)),
 answer = (M-1)*['L'])


puzzle1 = SlideDomain((1,2,3,7)+(8,4,5,6)+(9,0,10,11)+(12,13,14,15),
 answer = ['L', 'U', 'R', 'R', 'R', 'U', 'L', 'L', 'L'])


puzzle2 = SlideDomain((1,2,3,7)+(8,4,5,6)+(9,10,11,15)+(0,12,13,14),
 answer = ['R', 'R', 'R', 'U', 'L', 'L',
           'L', 'U', 'R', 'R', 'R', 'U', 'L', 'L', 'L'])


puzzle3 = SlideDomain((2,3,0,7)+(1,4,5,6)+(8,10,11,15)+(9,12,13,14),
 answer = ['L', 'L', 'D', 'D', 'D',
           'R', 'R', 'R', 'U', 'L', 'L',
           'L', 'U', 'R', 'R', 'R', 'U', 'L', 'L', 'L'])


puzzle4 = SlideDomain((2,3,7,6)+(1,4,5,0)+(8,10,11,15)+(9,12,13,14),
 answer = ['U', 'L', 'L', 'L', 'D', 'D', 'D',
           'R', 'R', 'R', 'U', 'L', 'L',
           'L', 'U', 'R', 'R', 'R', 'U', 'L', 'L', 'L'])


puzzle5 = SlideDomain((0,4,11,6)+(1,2,7,3)+(5,12,8,14)+(9,13,15,10),
 answer = ['R', 'D', 'R', 'U', 'R', 'D', 'L', 'L', 'L',
           'D', 'R', 'R', 'R', 'D', 'L', 'L', 'L', 'U',
           'R', 'D', 'R', 'U', 'R', 'U', 'L', 'U', 'L',
           'D', 'L', 'U'])


puzzle6 = SlideDomain((1,10,15,4)+(13,6,3,8)+(2,9,12,7)+(14,5,0,11),
  first = False,
 answer = ['U', 'L', 'L', 'U', 'R', 'R', 'U', 'L', 'D',
           'D', 'D', 'L', 'U', 'R', 'R', 'U', 'U', 'R',
           'D', 'D', 'D', 'L', 'U', 'U', 'R', 'U', 'L',
           'L', 'D', 'L', 'D', 'R', 'R', 'R', 'D'])


puzzle7 = SlideDomain((1,4,10,15)+(13,3,8,6)+(2,12,7,9)+(14,5,0,11),
  first = False,
 answer = 50*[0])   # Answer not given here but is at most 50 steps


puzzle8 = SlideDomain((15,11,13,12)+(14,10,9,5)+(2,6,8,1)+(3,7,4,0),
 answer = 100*[0])  # Answer not given but is at most 100 (?) steps


# Example problem list

problems = [ puzzle0, puzzle1, puzzle2,
            puzzle3, puzzle4, puzzle5, puzzle6,
            puzzle7, puzzle8
    ]


# MAIN FUNCTION

if __name__ == "__main__":
    example = problems[1]
    print ('SLIDE PUZZLE DOMAIN');                           print()
    print ('EXAMPLE START STATE:'); example.show();          print()
    print ('GOAL STATE:'); SlideDomain(example.goal).show(); print()
    print ('STORED ANSWER:'); print (example.answer);        print()

