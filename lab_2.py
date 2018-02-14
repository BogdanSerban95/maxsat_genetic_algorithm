import argparse
import time
from maxsat_clause import MaxSatClause, MaxSat

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
        clause = MaxSatClause(args.clause)
        print(clause.check_sat(args.assignment))
    elif question == 2:
        max_sat = MaxSat()
        max_sat.load_clauses(args.wdimacs)
        print(max_sat.count_sat_clauses(args.assignment))
    else:
        print('Incorrect question number.')

    print('Elapsed time: {}'.format(time.time() - start_time))
