from collections import defaultdict


class Constraints:
    def __init__(self, employees_db, employees, shifts):
        self.employees_db = employees_db
        self.employees = employees
        self.shifts = shifts

    # Hard constraint 1: primary ppo protected
    def hc1_primary_pto_protected(self):
        c = 0
        # iterate thru employee, shifts and check each shift against PPTO
        for i in range(len(self.shifts)):
            if (
                self.shifts[i][1]
                in self.employees_db[self.employees[i][0]]["PTO"]["Primary"]
            ):
                if self.shifts[i][0] != "OFF":
                    c += 1
        return c

    # Hard constraint 2: all shifts filled
    def hc2_all_shifts_filled(self):
        c = 0
        ###
        return c

    # Hard constraint 3: all roles valid
    def hc3_valid_roles(self):
        """check if employees are qualified for shift role and return # invalid shifts"""
        c = 0
        for i in range(len(self.shifts)):
            if (
                self.shifts[i][0]
                not in self.employees_db[self.employees[i][0]]["roles"]
            ):
                c += 1
        return c

    # Soft constraint 1: No double backing
    def sc1_no_double_back(self):
        """check if 3->1 shifts occur and return # violations"""
        c = 0
        # for i in range(len(self.shifts)):
        #     if self.shifts[i] == 3 and self.shifts[i+1] == 1 and self.employees[i][0] == self.employees[i+1][0]:
        #         c += 1
        return c

    # Soft constraint 2: Max 4 weekend days/schedule
    def sc2_max_4_weekends(self):
        """check if employees have >4 weekend shifts"""
        c = 0
        weekend_shifts = defaultdict(int)

        for employee, shift in list(zip(self.employees, self.shifts)):
            if (employee[1] == 0 or employee[1] == 7) and (shift != 0):  # weekend shift
                weekend_shifts[employee[0]] += 1
        for employee in weekend_shifts.keys():
            if weekend_shifts[employee] > 4:
                c += 1

        return c

    # Soft constraint 3: Minimal split weekends
    def sc3_min_split_weekends(self):
        c = 0
        # for day in weekend_days:
        # for i in range(len(employees)):
        return c

    # Soft constraint 4: No 7+ day stretches
    def sc4_no_7_days(self):
        """Check that no employee works a 7 day stretch"""
        c = 0
        consecutive_count = 0
        current_employee = self.employees[0][0]
        for i in range(len(self.employees)):
            if self.employees[i][0] == current_employee:
                if self.shifts[i] != 0:
                    consecutive_count += 1
                else:
                    consecutive_count = 0
            else:
                current_employee = self.employees[i][0]
                consecutive_count = 1
            if consecutive_count == 7:
                c += 1
        return c

    # Soft constraint 5: Secondary schedule requests
    def sc5_secondary_sched_reqs(self):
        c = 0
        # iterate thru employee, shifts and check each shift against PPTO
        # for i in range(len(self.shifts)):
        #     if self.shifts[i][1] in self.employees_db[self.employees[i][0]]['requests']['Off']:
        #         c += 1
        return c

    # Soft constraint 6: Shift distribution equal between team members
    def sc6_shift_dist_equal(self):
        "Check that employees have an even distribution of shifts"
        # calculate mean # of shifts per person
        shift_count = 0
        for shift in self.shifts:
            if shift != 0:  # is not a day off
                shift_count += 1
            else:
                pass
        mean_shifts = shift_count / len(self.employees_db.keys())

        # count individual shift totals
        individual_shifts = [0] * len(
            self.employees_db.keys()
        )  # array of 0 shifts for each employee
        for i in range(len(self.employees_db.keys())):
            for n in range(28 * i, 28 * (i + 1)):
                if self.shifts[n] != 0:
                    individual_shifts[i] += 1

        # average squared distance of each person's shift count from the mean
        sq_dists = sum([(n - mean_shifts) ** 2 for n in individual_shifts])
        mean_sq_dist = sum(sq_dists) / len(sq_dists)

        return mean_sq_dist

    # Soft constraint 7: Maximize contiguous morning vs evening stretches
    def sc7_max_contiguous_stretches(self):
        c = 0
        ###
        return c

    # Soft constraint 8: Minimize PM -> Swing and Swing -> AM transitions
    def sc8_min_pm_swing_am(self):
        c = 0
        ###
        return c

    # Soft constraint 9: Minimal split weekdays off
    def sc9_min_split_weekdays_off(self):
        c = 0
        ###
        return c

    def hard_constraint_cost(self, constraints="all"):
        """select and apply hard constraints then sum penalty scores"""
        all_constraints = [
            self.hc1_primary_pto_protected,
            self.hc2_all_shifts_filled,
            self.hc3_valid_roles,
        ]
        if constraints == "all":
            constraints = [i + 1 for i in range(len(all_constraints))]
        c = 0
        violations = defaultdict(int)  # log individual violation types

        for hc_number in constraints:
            temp_c = 0
            temp_c += all_constraints[hc_number - 1]()
            c += temp_c
            violations[hc_number] += temp_c
        return (c, violations)

    def soft_constraint_cost(self, constraints="all"):
        """select and apply hard constraints then sum penalty scores"""
        all_constraints = [
            self.sc1_no_double_back,
            self.sc2_max_4_weekends,
            self.sc3_min_split_weekends,
            self.sc4_no_7_days,
            self.sc5_secondary_sched_reqs,
            self.sc7_max_contiguous_stretches,
            self.sc8_min_pm_swing_am,
            self.sc9_min_split_weekdays_off,
        ]
        if constraints == "all":
            constraints = [i + 1 for i in range(len(all_constraints))]
        c = 0
        violations = defaultdict(int)  # log individual violation types

        for sc_number in constraints:
            temp_c = 0
            temp_c += all_constraints[sc_number - 1]()
            c += temp_c
            violations[sc_number] += temp_c

        return (c, violations)

    def total_cost(
        self, hard_constraints, soft_constraints
    ):  # expects constraints e.g. [[1, 2], [2,3]]
        """Calculate penalty cost of a schedule"""
        # Set weights, select constraints and calculate hard and soft costs
        hard_weight = 1
        hard_cost = self.hard_constraint_cost(hard_constraints)[
            0
        ]  # (total, {constraint:total})[0]

        soft_weight = 1
        soft_cost = self.soft_constraint_cost(soft_constraints)[
            0
        ]  # (total, {constraint:total})[0]

        # Return total weighted cost function
        return hard_weight * hard_cost + soft_weight * soft_cost
