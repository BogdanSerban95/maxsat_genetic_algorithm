import math
import numpy as np
import sys, argparse
import time


def check_sat(clause, assignment):
    split_clause = np.array(clause.split(' '))
    split_clause = split_clause[1: len(split_clause) - 1].astype(int)
    abs_split_claus = np.fabs(split_clause).astype(int)

    for i in range(len(split_clause)):
        if split_clause[i] > 0 and assignment[abs_split_claus[i] - 1] == '1':
            return 1
        elif split_clause[i] < 0 and assignment[abs_split_claus[i] - 1] == '0':
            return 1

    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SATMAX genetic algorithm.')
    parser.add_argument('-question', help='Question number', type=int, required=True)
    parser.add_argument('-clause', help='A SATMAX clause description', type=str)
    parser.add_argument('-assignment', help='An assignment as a bitstring', type=str)

    args = parser.parse_args()
    question = args.question
    start_time = time.time()

    if question == 1:
        print(check_sat(args.clause, args.assignment))
    else:
        print('Incorrect question number.')

    print('Elapsed time: {}'.format(time.time() - start_time))
