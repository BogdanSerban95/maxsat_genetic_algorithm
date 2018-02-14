import math
import numpy as np
import sys, argparse
import time
import random


def check_sat(clause, abs_clause, assignment):
    for i in range(len(clause)):
        cl_idx = abs_clause[i] - 1
        if clause[i] > 0 and assignment[cl_idx] == '1':
            return 1
        elif clause[i] < 0 and assignment[cl_idx] == '0':
            return 1
    return 0


def count_sat_clauses(in_clauses, abs_in_clauses, assignment):
    total = 0
    for i in range(len(in_clauses)):
        total += check_sat(in_clauses[i], abs_in_clauses[i], assignment)
    return total


def parse_wdimacs_file(file_name):
    out_clauses = []
    abs_out_clauses = []
    n = 0
    m = 0
    with open(file_name, 'r') as input_file:
        for line in input_file.readlines():
            if 'c' not in line:
                clause = parse_clause_line(line)
                out_clauses.append(clause)
                abs_out_clauses.append(np.fabs(clause).astype(int))
            elif 'p cnf' in line or 'p wcnf' in line:
                split = line.split(' ')
                n = int(split[2])
                m = int(split[3])

    return n, m, np.array(out_clauses), np.array(abs_out_clauses)


def parse_clause_line(clause_line):
    split = np.array(clause_line.split(' '))
    return split[1: len(split) - 1].astype(int)


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
        abs_split_clause = np.fabs(split_clause).astype(int)
        print(check_sat(split_clause, args.assignment, split_clause))
    elif question == 2:
        (num_var, num_clauses, clauses, clauses_abs) = parse_wdimacs_file(args.wdimacs)
        print('File load time: {}'.format(time.time() - start_time))
        start_time = time.time()
        max_num = 2 ** num_var - 1
        num = random.randint(0, max_num)
        bits = bin(num)[2:].zfill(num_var)
        start_time = time.time()

        print(count_sat_clauses(clauses, clauses_abs, bits))
    else:
        print('Incorrect question number.')

    print('Elapsed time: {}'.format(time.time() - start_time))
