import random

MODEST = 1
FAIR = 2
GREEDY = 3

# TODO use scala?

class Agent():
    # preferences can be 1/3, 1/2, 2/3
    # valid matchings: 
    #   1, 3
    #   2, 2
    #   3, 1
    def __init__(self, pref=random.randint(1,3)): 
        self.pref = pref

    def is_compatible(self, other):
        return self.pref + other.pref == 4
        return self.pref == MODEST == other.pref == GREEDY or \
               self.pref == FAIR == other.pref == FAIR or \
               self.pref == GREEDY == other.pref == FAIR
    
    def __repr__(self):
        if self.pref == MODEST:
            return f"1/3"
        elif self.pref == FAIR:
            return f"1/2"
        elif self.pref == GREEDY:
            return f"2/3"
        
class Population():
    # TODO: there's a good way to generalize this, but for now I just want to ensure that the weights work out
    # could use an enum: Even, normal, inverse, custom?
    # for now just a % of the time that I want a good boi
    def __init__(self, n=100, distribution=0.6, _pop=None):
        if _pop:
            self._population = _pop
        else: 
            self._population = []
            for _ in range(n):
                if random.random() < distribution:
                    self._population.append(Agent(pref=FAIR))
                else:
                    pref = MODEST if random.random() < 0.5 else GREEDY
                    self._population.append(Agent(pref=pref))

    def get_distr(self): 
        # TODO replace with thing
        counts = {
            MODEST: 0,
            FAIR: 0,
            GREEDY: 0
            }
        for a in self._population:
            counts[a.pref] += 1

        return counts

        

    # TODO: add some generalizaiton about generations
        
def match_all(_population):
    new_pop = []
    num_compat = 0
    num_incompat = 0
    while len(_population) > 1:
        # pluck w/o repetition 

        fst = _population.pop(random.choice(range(len(_population))))
        snd = _population.pop(random.choice(range(len(_population))))
                            
        if fst.is_compatible(snd):
            # print((fst, snd))
            num_compat += 1
            new_pop.append(fst)
            new_pop.append(snd)
        else:
            num_incompat += 1

    
    return (Population(_pop=new_pop), num_compat, num_incompat)        

# population = Population(n=100)

# match_all(population._population)

# TODO: want to simulate


import matplotlib.pyplot as plt
import numpy as np


ms, fs, gs = [],[],[]
epochs=10
for epoch in range(epochs):
    p = Population(n=40000)
    new_pop, num_compat, num_incompat = match_all(p._population)
    print(f"remaining population: {len(new_pop._population)}, # compatible: {num_compat}, # incompatible: {num_incompat}")
    d = new_pop.get_distr()
    ms.append(d[MODEST])
    fs.append(d[FAIR])
    gs.append(d[GREEDY])

print(sum(ms), sum(fs), sum(gs))
bins = np.linspace(0, 20000, epochs)
plt.hist(ms, bins, alpha=0.5, align='left', label='modest')
plt.hist(fs, bins, alpha=0.5, label='fair')
plt.hist(gs, bins, alpha=0.5, align='right', label='greedy')
plt.legend(loc='upper right')
plt.show()