import argparse
import time
from max_sat import MaxSatClause, MaxSat
from genetic_algorithm import MaxSatGeneticAlgorithm

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SATMAX genetic algorithm.')
    parser.add_argument('-question', help='Question number', type=int, required=True)
    parser.add_argument('-clause', help='A SATMAX clause description', type=str)
    parser.add_argument('-assignment', help='An assignment as a bitstring', type=str)
    parser.add_argument('-wdimacs', help='Name of file on WDIMACS format', type=str)
    parser.add_argument('-time_budget', help='Number of seconds per repetition', type=float)
    parser.add_argument('-repetitions', help='The number of repetitions of the algorithm', type=int)

    args = parser.parse_args()
    question = args.question

    if question == 1:
        clause = MaxSatClause(args.clause)
        print(clause.check_sat(args.assignment))
    elif question == 2:
        max_sat = MaxSat()
        max_sat.load_clauses(args.wdimacs)
        print(max_sat.count_sat_clauses(args.assignment))
    elif question == 3:
        max_sat = MaxSat()
        max_sat.load_clauses(args.wdimacs)
        print('Clauses loaded...')

        genetic_alg = MaxSatGeneticAlgorithm(pop_size=20, tourn_size=4, mutation_rate=1.5, time_limit=args.time_budget,
                                             max_sat_instance=max_sat)
        for i in range(args.repetitions):
            start_time = time.time()
            t, nsat, xsat = genetic_alg.run_ga()

            print(t, nsat)
            print('Elapsed time: {}'.format(time.time() - start_time))
    else:
        print('Incorrect question number.')
