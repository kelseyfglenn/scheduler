# Employee object definition and DB builder

import json


# Employee class
class Employee():
    def __init__(self, name, roles = [], PTO = []):
        self.name = name
        self.roles = roles
        self.PTO = PTO # requested PTO dates -- can remove any assigned PTO dates from employee/shift list before model runs
    
    def add_roles(self, roles):
        for role in roles:
            if role not in self.roles:
                self.roles.append(role)
    
    def remove_roles(self, roles):
        new_roles = []
        removed_roles = []
        for role in self.roles:
            if role not in roles:
                new_roles.append(role)
            else:
                removed_roles.append(role)
        self.roles = new_roles
        print('Removed:\n')
        print(', '.join(removed_roles))
    
    def set_roles(self, roles):
        self.roles = roles
    
    def add_PTO(self, dates):              
        for date in dates:
            if date not in self.PTO:
                self.PTO.append(date)
    
    def remove_PTO(self, dates):
        new_dates = []
        removed_dates = []
        for date in self.PTO:
            if date not in dates:
                new_dates.append(date)
            else:
                removed_dates.append(date)
        self.PTO = new_dates
        print('Removed:\n')
        print(', '.join(removed_dates))
    
    def set_PTO(self, dates):
        self.PTO = dates


def generate_employee_db(employee_names_file, employee_db_file):
    """Generates json of employees from name list w/ empty role and PTO properties"""
    employee_dict = {}
    with open(employee_names_file) as infile:
        for name in infile:
            employee_dict[name[:-1]] = {'roles' : ['OFF'], # go to -1 index to drop \n, everyone has 'OFF' role by default
                                'PTO' : []}
    with open(employee_db_file, 'w') as outfile:
        json.dump(employee_dict, outfile)
        

def populate_test_db(employees_db, all_roles):
    """Populate a db of just employee names with random role and PTO values"""
    
    for employee in employees_db.keys():
        all_dates = list(range(28))
        with open('roles.txt', 'r') as f:
            for line in f:
                all_roles.append(line[:-1]) # :-1 to drop newline

        # pick random n 1-4 and randomly add that many roles
        n_roles = random.randint(1,4)
        roles = random.sample(all_roles, n_roles)

        # pick random n 0-7 and randomly add that many PTO days
        n_PTO = random.randint(0,7)
        PTO = random.sample(all_dates, n_PTO)
        
        employees_db[employee]['roles'].extend(roles)
        employees_db[employee]['PTO'].extend(PTO)
    
    return employees_db