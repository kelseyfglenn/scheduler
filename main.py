from __future__ import print_function
import math
import random
from collections import defaultdict
from simanneal import Annealer

employees = {
    'Adam' : {'roles' : [0, 1, 2]},
    'Julie' : {'roles' : [0, 2, 3]},
    'Dave' : {'roles' : [0, 1, 3]},
    'Alice' : {'roles' : [0, 2]}
}

# (employee, date) for indexing shifts
employees_input = [(key, s) for key in employees.keys() for s in range(7) ]


def feasible(employee, shift):
    if shift not in employees[employee]['roles']:
        return 0
    else:
        return 1
       

def cost(employees, shifts):
    """Calculate penalty cost of a schedule"""
    cost = 0
    
    # feasibility test
    for i in range(len(shifts)):
        if feasible(employees[i][0], shifts[i]) == 0:
            # cost += 1 # count penalties to compare infeasible solutions
            return None # non-numeric to distinguish from high energy solutions
    
    # if shift 3 into shift 1 with the same employee, penalize
    for i in range(len(shifts)):
        if shifts[i] == 3 and shifts[i+1] == 1 and employees[i][0] == employees[i+1][0]:
            cost += 1
    
    return cost

    
class Scheduler(Annealer):
    def __init__(self, state, employees):
        self.employees = employees
        super(Scheduler, self).__init__(state)

    def move(self):
        """Swap two shift assignments"""
        initial_energy = self.energy()
        
        a = random.randint(0, len(self.state) - 1)
        b = random.randint(0, len(self.state) - 1)
        self.state[a], self.state[b] = self.state[b], self.state[a]
        return self.energy() - initial_energy

    def energy(self):
        """Rate schedule quality"""
        e = cost(self.employees, self.state)
        if e == None: 
            return 1000 # guarantee it's not accepted
        else:
            return e


if __name__ == '__main__':
    # list of shift inputs
    shifts = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # randomized initial assignments
    init_state = shifts
    random.shuffle(init_state)
    
    sched = Scheduler(init_state, employees_input)
    sched.set_schedule(sched.auto(minutes=0.2))
    sched.copy_strategy = "slice"
    state, e = sched.anneal()
    
    
    print('Adam')
    # print(employees_input[0:7])
    print(list(state)[:7])
    print('Julie')
    # print(employees_input[7:14])
    print(list(state)[7:14])
    print('Dave')
    # print(employees_input[14:21])
    print(list(state)[14:21])
    print('Alice')
    # print(employees_input[21:])
    print(list(state)[21:])
