# Hospital scheduling app by Kelsey Glenn
# https://github.com/kelseyfglenn/scheduler

import json
import random
import pandas as pd
from shifts import Shifts
from constraints import Constraints
from simanneal import Annealer


# inputs
employees_db_file = "../output/test_db.json"
shifts_file = "../shifts.csv"


with open(employees_db_file) as f:
    employees_db = json.load(f)
employees = [
    (name, i) for name in employees_db.keys() for i in range(28)
]  # (name, date) * (28 days * n employees)
n_employees = len(employees_db.keys())
shifts = Shifts(
    shifts_file, n_employees
).generate()  # convert shift CSV into list of (role, date) tuples

hard_constraints = "all"
soft_constraints = "all"


class Scheduler(Annealer):
    def __init__(
        self, employees_db, employees, shifts, hard_constraints, soft_constraints
    ):
        self.employees_db = employees_db
        self.employees = employees
        self.shifts = shifts
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
        if e is None:
            return 1000  # guarantee it's not accepted
        else:
            return e

    def evaluate(self):
        """Summarize constraint violations"""
        hard_cost = self.constraints.hard_constraint_cost(
            hard_constraints
        )  # (total, {constraint:total})
        soft_cost = self.constraints.soft_constraint_cost(
            soft_constraints
        )  # (total, {constraint:total})
        print(hard_cost)
        print(soft_cost)


# initialize employees, shift state, execute annealing and generate output CSV
if __name__ == "__main__":
    # randomized initial assignments
    init_state = shifts
    random.shuffle(init_state)

    # execute annealing algo
    sched = Scheduler(
        employees_db, employees, init_state, hard_constraints, soft_constraints
    )
    sched.set_schedule(sched.auto(minutes=0.2))
    sched.copy_strategy = "slice"
    state, e = sched.anneal()
    sched.evaluate()

    # format schedule for output
    output = pd.DataFrame(employees, columns=["employee", "date"])
    output["shift"] = state
    output = output.set_index(["employee", "date"]).unstack(level=[1]).reset_index()
    output.columns = output.columns.get_level_values(0)
    output.columns = range(29)
    output = output.rename(columns={0: "Employee"})
    output.to_csv("output/schedule.csv")
