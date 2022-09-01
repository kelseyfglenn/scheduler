from __future__ import print_function
import math
import random
from collections import defaultdict
from simanneal import Annealer
import pandas as pd

def hc1_valid_roles(employees_db, employees, shifts):
    c = 0
    for i in range(len(shifts)):
        if shifts[i] not in employees_db[employees[i][0]]['roles']:
            c += 1
    return c
       
# Soft constraint 1: No double backing
def sc1_double_back(employees, shifts):
    c = 0
    # for i in range(len(shifts)):
    #     if shifts[i] == 3 and shifts[i+1] == 1 and employees[i][0] == employees[i+1][0]:
    #         c += 1
    return c

# Soft constraint 2: Max 4 weekend days/schedule
# # count weekend shifts
# weekend_shifts = df[(((df.date == 0) | (df.date == 6) | (df.date == 7) | (df.date == 13) | (df.date == 14) | (df.date == 20) | (df.date == 21) | (df.date == 27)) & (df['shift'] != 0))].groupby('employee').count()        
# c2 += len(weekend_shifts[weekend_shifts['shift'] > 4]) # +1 for every instance of 4+ weekend days

# # Soft constraint 3: Minimal split weekends
# for day in weekend_days:
#     for i in range(len(employees)):
        

# Soft constraint 4: No 7+ day stretches
def sc4_no_7_days(employees, shifts):
    c = 0
    consecutive_count = 0    
    current_employee = employees[0][0]
    for i in range(len(employees)):
        if employees[i][0] == current_employee:
            if shifts[i] != 0:
                consecutive_count += 1
            else:
                consecutive_count = 0
        else:
            current_employee = employees[i][0]
            consecutive_count = 1
        if consecutive_count == 7:
            c += 1
    return c

def cost(employees_db, employees, shifts):
    """Calculate penalty cost of a schedule"""
    hard_cost, soft_cost = 0, 0
    hard_weight, soft_weight = 1, 1
    
    # weekend_days = [0, 6, 7, 13, 14, 20, 21, 27]
    # zip employees, dates and shifts into a df
    df = pd.DataFrame(employees_input, columns=['employee', 'date'])
    df['shift'] = shifts
      
    # sum constraint penalties
    hard_cost = hc1_valid_roles(employees_db, employees, shifts)
    soft_cost = sc1_double_back(employees, shifts) + sc4_no_7_days(employees, shifts)

    # Return total weighted cost function
    return hard_weight * hard_cost + soft_weight * soft_cost
    
 

    
class Scheduler(Annealer):
    def __init__(self, employees_db, state, employees):
        self.employees_db = employees_db
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
        e = cost(self.employees_db, self.employees, self.state)
        if e == None: 
            return 1000 # guarantee it's not accepted
        else:
            return e


employees_db = {
    'Adam' : {'roles' : [0, 1, 2]},
    'Julie' : {'roles' : [0, 2, 3]},
    'Dave' : {'roles' : [0, 1, 3]},
    'Alice' : {'roles' : [0, 2]}
}
employees_input = [(key, s) for key in employees_db.keys() for s in range(28) ]
shifts = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] * 4

if __name__ == '__main__':
    # list of shift inputs
    # shifts = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # randomized initial assignments
    init_state = shifts
    random.shuffle(init_state)
    
    sched = Scheduler(employees_db, init_state, employees_input)
    sched.set_schedule(sched.auto(minutes=0.2))
    sched.copy_strategy = "slice"
    state, e = sched.anneal()
    
    
    print('Adam')
    # print(employees_input[0:7])
    print(list(state)[:28])
    print('Julie')
    # print(employees_input[7:14])
    print(list(state)[28:56])
    print('Dave')
    # print(employees_input[14:21])
    print(list(state)[56:84])
    print('Alice')
    # print(employees_input[21:])
    print(list(state)[84:112])
