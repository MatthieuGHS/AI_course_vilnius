def update_jugs(state, t, i, j):
    if i != j :
        lst = list(state)
        lst[i]-=t
        lst[j]+=t
        return tuple(lst)
    else:
        lst = list(state)
        lst[i] += t
        return tuple(lst)

def pour(state, sizes, i, j):
    if i == j : return None
    t = min(state[i], sizes[j]-state[j])
    if t > 0 :
        return update_jugs(state, t, i, j)
    else:
        return None

def fill(state, size, i):
    if state[i] < size[i]:
        return update_jugs(state, size[i]-state[i], i, i)
    else:
        return None

def empty(state, i):
   lst = list(state)
   lst[i]=0
   return tuple(lst) 

class JugDomain:
    def __init__(self, start, sizes, goal, source=True):
        self.sizes = sizes
        self.start = start
        self.source = source
        self.goal = goal

    def is_goal(self, state):
        times, obj = [int(elt) for elt in self.goal.split("x")]
        c = 0
        for elt in state:
            if elt == obj :
                c+=1
        return c==times

    def go_next(self, state):
        succ = []
        n = len(self.sizes)
        if self.source :
            for i in range(n):
                new = fill(state, self.sizes, i)
                if new is not None :
                    succ.append((("fill", i), new))
                new = empty(state, i)
                if new is not None :
                    succ.append((("empty", i), new))
        for i in range(n):
            for j in range(n):
                new = pour(state, self.sizes, i, j)
                if new is not None :
                    succ.append((("pour", i, j), new))
        return succ


#### PROBLEMS ####


jug0 = JugDomain((0, 0), (3, 5), "1x4", source=True)

jug1 = JugDomain((1, 0, 19), (7, 13, 19), "2x10", source=False)

jug2 = JugDomain((0, 0, 89), (34, 55, 89), "1x54", source=False)

jug3 = JugDomain((0, 0, 0, 36), (9, 18, 23, 36), "3x12", source=False)

problems = [jug0, jug1, jug2, jug3]
