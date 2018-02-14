import numpy as np


class MaxSat(object):
    def __init__(self):
        self.num_clauses = 0
        self.num_vars = 0
        self.clauses = None

    def load_clauses(self, file_name):
        clauses = []
        with open(file_name, 'r') as input_file:
            for line in input_file.readlines():
                if 'c' not in line:
                    clauses.append(MaxSatClause(line))
                elif line.startswith('p'):
                    split = line.split(' ')
                    self.num_vars = int(split[2])
                    self.num_clauses = int(split[3])
        self.clauses = np.array(clauses)

    def count_sat_clauses(self, assignment):
        total = 0
        for clause in self.clauses:
            total += clause.check_sat(assignment)
        return total


class MaxSatClause(object):
    def __init__(self, clause_line):
        split = np.array(clause_line.split(' '))
        self.var_list = split[1: len(split) - 1].astype(int)
        self.abs_var_list = np.fabs(self.var_list).astype(int)
        self.length = len(self.var_list)

    def check_sat(self, assignment):
        for i in range(self.length):
            cl_idx = self.abs_var_list[i] - 1
            if self.var_list[i] > 0 and assignment[cl_idx] == '1':
                return 1
            elif self.var_list[i] < 0 and assignment[cl_idx] == '0':
                return 1
        return 0
