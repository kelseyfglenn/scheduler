# Hospital scheduling app by Kelsey Glenn
# https://github.com/kelseyfglenn/scheduler

import random
from simanneal import Annealer
import pandas as pd
from constraints import Constraints


# test inputs
hard_constraints = 'all'
soft_constraints = 'all'
employees_db = {
    'Adam' : {'roles' : [0, 1, 2]},
    'Julie' : {'roles' : [0, 2, 3]},
    'Dave' : {'roles' : [0, 1, 3]},
    'Alice' : {'roles' : [0, 2]}
}
employees_input = [(key, s) for key in employees_db.keys() for s in range(28) ]
shifts_input = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] * 4


class Scheduler(Annealer):
    def __init__(self, employees_db, employees, shifts, hard_constraints, soft_constraints):
        self.employees_db = employees_db
        self.employees = employees_input
        self.shifts = shifts_input
        self.hard_constraints = hard_constraints
        self.soft_constraints = soft_constraints
        self.constraints = Constraints(self.employees_db, self.employees, self.shifts)
        super(Scheduler, self).__init__(shifts)


    def move(self):
        """Swap two shift assignments"""
        initial_energy = self.energy()
        
        a = random.randint(0, len(self.shifts) - 1)
        b = random.randint(0, len(self.shifts) - 1)
        self.shifts[a], self.shifts[b] = self.shifts[b], self.shifts[a]
        return self.energy() - initial_energy

    
    def energy(self):
        """Rate schedule quality"""
        e = self.constraints.total_cost(self.hard_constraints, self.soft_constraints)
        if e == None: 
            return 1000 # guarantee it's not accepted
        else:
            return e


    def evaluate(self):
        """Summarize constraint violations"""
        hard_cost = self.constraints.hard_constraint_cost(hard_constraints) # (total, {constraint:total})
        soft_cost = self.constraints.soft_constraint_cost(soft_constraints) # (total, {constraint:total})
        print(hard_cost)
        print(soft_cost)


# initialize employees, shift state, execute annealing and generate output CSV
if __name__ == '__main__':
    # randomized initial assignments
    init_state = shifts_input
    random.shuffle(init_state)
    
    # execute annealing algo
    sched = Scheduler(employees_db, employees_input, init_state, hard_constraints, soft_constraints)
    sched.set_schedule(sched.auto(minutes=0.2))
    sched.copy_strategy = "slice"
    state, e = sched.anneal()
    sched.evaluate()
    
    # format schedule for output
    output = pd.DataFrame(employees_input, columns=['employee', 'date'])
    output['shift'] = state
    output = output.set_index(['employee', 'date']).unstack(level=[1]).reset_index()
    output.columns = output.columns.get_level_values(0)
    output.columns = range(29)
    output = output.rename(columns={0:'Employee'})
    output.to_csv('schedule.csv')

