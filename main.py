# Hospital scheduling app by Kelsey Glenn
# https://github.com/kelseyfglenn/scheduler

import random
from simanneal import Annealer
import pandas as pd


def hc1_valid_roles(employees_db, employees, shifts):
    """check if employees are qualified for shift role and return # invalid shifts"""
    c = 0
    for i in range(len(shifts)):
        if shifts[i] not in employees_db[employees[i][0]]['roles']:
            c += 1
    return c

    
# Soft constraint 1: No double backing
def sc1_no_double_back(employees, shifts):
    """check if 3->1 shifts occur and return # violations"""
    c = 0
    # for i in range(len(shifts)):
    #     if shifts[i] == 3 and shifts[i+1] == 1 and employees[i][0] == employees[i+1][0]:
    #         c += 1
    return c


# Soft constraint 2: Max 4 weekend days/schedule
def sc2_max_4_weekends(employees, shifts):
    """check if employees have >4 weekend shifts"""
    c = 0
    weekend_days = [0, 6, 7, 13, 14, 20, 21, 27]
    # # count weekend shifts
    # weekend_shifts = df[(((df.date == 0) | (df.date == 6) | (df.date == 7) | (df.date == 13) | (df.date == 14) | (df.date == 20) | (df.date == 21) | (df.date == 27)) & (df['shift'] != 0))].groupby('employee').count()        
    # c2 += len(weekend_shifts[weekend_shifts['shift'] > 4]) # +1 for every instance of 4+ weekend days
    return c


# Soft constraint 3: Minimal split weekends
def sc3_min_split_weekends(employees, shifts):
    c = 0
    # for day in weekend_days:
        # for i in range(len(employees)):
    return c


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
    
    # zip employees, dates and shifts into a df
    df = pd.DataFrame(employees_input, columns=['employee', 'date'])
    df['shift'] = shifts
      
    # sum constraint penalties
    hard_cost = hc1_valid_roles(employees_db, employees, shifts)
    soft_cost = sc1_no_double_back(employees, shifts) + sc2_max_4_weekends(employees, shifts) + sc3_min_split_weekends(employees, shifts) + sc4_no_7_days(employees, shifts)

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


# test inputs
employees_db = {
    'Adam' : {'roles' : [0, 1, 2]},
    'Julie' : {'roles' : [0, 2, 3]},
    'Dave' : {'roles' : [0, 1, 3]},
    'Alice' : {'roles' : [0, 2]}
}
employees_input = [(key, s) for key in employees_db.keys() for s in range(28) ]
shifts = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] * 4


# initialize employees, shift state, execute annealing and generate output CSV
if __name__ == '__main__':
    # randomized initial assignments
    init_state = shifts
    random.shuffle(init_state)
    
    # execute annealing algo
    sched = Scheduler(employees_db, init_state, employees_input)
    sched.set_schedule(sched.auto(minutes=0.2))
    sched.copy_strategy = "slice"
    state, e = sched.anneal()
    
    # format schedule for output
    output = pd.DataFrame(employees_input, columns=['employee', 'date'])
    output['shift'] = state
    output = output.set_index(['employee', 'date']).unstack(level=[1]).reset_index()
    output.columns = output.columns.get_level_values(0)
    output.columns = range(29)
    output = output.rename(columns={0:'Employee'})
    output.to_csv('schedule.csv')

