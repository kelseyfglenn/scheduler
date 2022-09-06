import pandas as pd
       
# shift_map = {'AM' : ['CAM1', 'IVAM1', 'IVAM2', 'IS'],
#                 'PM' : ['CPM', 'IVPM', 'CCPM1', 'CCPS'],
#                 'OFF' : ['PTO', 'PRO']}

class Shifts():
    def __init__(self, shifts_path):
        self.shifts_path = shifts_path

    def table_to_list(self):
        """convert table into list of (role, date) tuples"""
        shifts = pd.read_csv(self.shifts_path)
        shift_list = []
        for date in shifts.columns[1:]: # go to each date column
            role_date = shifts[['ROLE', date]]
            new_shifts = []
            for i in range(len(role_date)): # go through each role/row
                n_shifts = role_date.iloc[i][1] 
                for i in range(n_shifts): # repeat append for each n_shifts of the role needed that day
                    new_shifts.append((role_date.iloc[i][0], date))
    
            # add empty shifts for difference b/t # employees and # shifts required
            empty_shifts = len(employees_db.keys()) - len(new_shifts) # total possible - total 
            for i in range(empty_shifts):
                new_shifts.append(('OFF', date))
                
            shift_list.extend(new_shifts)
        
        return shift_list

    def generate(self):
        return self.table_to_list(self.shifts_path)
    