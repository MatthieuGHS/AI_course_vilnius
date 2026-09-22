from state_search_thin import StateSearch, path_length
from slide_domain_thin import problems, path_solved


# Run search and report computation time

import time
import cProfile


def run_strategy (strategy, model):
    """ Run a particular search problem. """
    tick = time.perf_counter()
    result = strategy(model)
    tock = time.perf_counter()

    # Output result
    elap = tock - tick
    print ('Time: %6.2f s using %s' % (elap, strategy.__name__.upper()))
    solution = path_solved(result)
    print ('Found %d step solution:' % len(solution))
    print (solution)


# Choose problem to solve
problem = problems[2]

# Construct a search model
start = problem.start
is_goal = problem.is_goal
go_next = problem.go_next

model = (start, is_goal, go_next, None)


# Create search object
so = StateSearch()
profile = False

# Run search using selected strategies
strategies = ( so.idps, so.bfgq, so.lcgq, )
for strategy in strategies:
    def go ():
        run_strategy (strategy, model)
    if profile:
        cProfile.runctx('go()', None, locals(), sort='time')
    else: go()


#########
# A* test
#
# If your implementation works,
#   problems[5] will be solved easily

print ("")
print ("A* TEST")

problem = problems[2]

start = problem.start
is_goal = problem.is_goal
go_next = problem.go_next
cost = problem.astar_cost
depth = len(problem.answer)

model = (start, is_goal, go_next, cost)

so = StateSearch(depth)
strategy = so.lcgq
run_strategy (strategy, model)

