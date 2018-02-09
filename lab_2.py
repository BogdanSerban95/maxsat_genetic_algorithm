import math
import numpy as np
import sys, argparse
import time
import random


def check_sat(clause, assignment):
    abs_split_clause = np.fabs(clause).astype(int)

    for i in range(len(clause)):
        if clause[i] > 0 and assignment[abs_split_clause[i] - 1] == '1':
            return 1
        elif clause[i] < 0 and assignment[abs_split_clause[i] - 1] == '0':
            return 1

    return 0


def count_sat_clauses(in_clauses, assignment):
    total = 0
    for clause in in_clauses:
        total += check_sat(clause, assignment)

    return total


def parse_wdimacs_file(file_name):
    out_clauses = []
    n = 0
    m = 0
    with open(file_name, 'r') as input_file:
        for line in input_file.readlines():
            if 'c' not in line:
                out_clauses.append(parse_clause_line(line))
            elif 'p cnf' in line or 'p wcnf' in line:
                split = line.split(' ')
                n = int(split[2])
                m = int(split[3])

    return n, m, out_clauses


def parse_clause_line(clause_line):
    split = np.array(clause_line.split(' '))
    split = split[1: len(split) - 1].astype(int)

    return split


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SATMAX genetic algorithm.')
    parser.add_argument('-question', help='Question number', type=int, required=True)
    parser.add_argument('-clause', help='A SATMAX clause description', type=str)
    parser.add_argument('-assignment', help='An assignment as a bitstring', type=str)
    parser.add_argument('-wdimacs', help='Name of file on WDIMACS format', type=str)

    args = parser.parse_args()
    question = args.question
    start_time = time.time()

    if question == 1:
        split_clause = parse_clause_line(args.clause)
        print(check_sat(split_clause, args.assignment))
    elif question == 2:
        (num_var, num_clauses, clauses) = parse_wdimacs_file(args.wdimacs)
        print(count_sat_clauses(clauses, args.assignment))
    else:
        print('Incorrect question number.')

    print('Elapsed time: {}'.format(time.time() - start_time))
