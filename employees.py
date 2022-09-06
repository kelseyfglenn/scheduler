class Employee():
    def __init__(self, name):
        self.name = name
        self.roles = []
        self.PTO = [] # requested PTO dates -- can remove any assigned PTO dates from employee/shift list before model runs
    
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
