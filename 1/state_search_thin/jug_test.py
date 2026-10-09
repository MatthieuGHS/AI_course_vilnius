from state_search_thin import StateSearch, path_actions
from jug_domain import problems


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
    print (f'Time: {elap:6.2f} s using {strategy.__name__.upper()}')
    solution = path_actions(result)
    print (f'Found {len(solution)} step solution:')
    print (solution)
    if result: print (f'Final state: {result[-1]}')


depth = 70
profile = False

for k, problem in enumerate(problems):
    print (f"\n========== problems[{k}] : sizes {problem.sizes}, start {problem.start}, goal {problem.goal} ==========\n")

    # Construct a search model
    start = problem.start
    is_goal = problem.is_goal
    go_next = problem.go_next

    model = (start, is_goal, go_next, None)

    # Create search object
    so = StateSearch(depth)

    # Run search using selected strategies
    strategies = ( so.bfgq, so.lcgq, )
    for strategy in strategies:
        def go ():
            run_strategy (strategy, model)
        if profile:
            cProfile.runctx('go()', None, locals(), sort='time')
        else: go()
