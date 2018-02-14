import time
import random
import numpy as np


class MaxSatGeneticAlgorithm(object):
    def __init__(self, pop_size, tourn_size, mutation_rate, time_limit, max_sat_instance):
        self.pop_size = pop_size
        self.time_limit = time_limit
        self.tourn_size = tourn_size
        self.mutation_rate = mutation_rate
        self.max_sat_instance = max_sat_instance
        self.ind_size = max_sat_instance.num_vars

        self.start_time = 0

        self.current_pop = None
        self.current_pop_fitness = None

    def generate_initial_population(self):
        self.current_pop = np.array([])
        self.current_pop_fitness = np.array([])
        max_num = 2 ** self.ind_size - 1

        for i in range(self.pop_size):
            num = random.randint(0, max_num)
            bits = bin(num)[2:].zfill(self.ind_size)
            self.current_pop = np.append(self.current_pop, bits)
            self.current_pop_fitness = np.append(self.current_pop_fitness,
                                                 self.max_sat_instance.count_sat_clauses(bits))

    def best_fit(self):
        max_idx = np.argmax(self.current_pop_fitness)
        return self.current_pop_fitness[max_idx], self.current_pop[max_idx]

    def mutate(self, bits_x):
        mutation_rate = self.mutation_rate / self.ind_size
        y = ''
        for bit in bits_x:
            prob = random.uniform(1, 0)
            y += self.bit_not(bit) if prob < mutation_rate else bit
        return y

    def tournament_selection(self):
        ind = np.random.randint(0, self.pop_size - 1, self.tourn_size)
        scores = self.current_pop_fitness[ind]

        winners = scores == max(scores)
        winner_pos = ind[winners][random.randint(0, len(scores[winners]) - 1)]
        return self.current_pop[winner_pos]

    def crossover_operator(self, bits_x, bits_y):
        z = ''
        for i in range(0, self.ind_size):
            z += str(random.randint(0, 1) if bits_x[i] != bits_y[i] else bits_x[i])

        return z

    def run_ga(self):
        t = 0
        fbest = 0
        xbest = ''
        generations = 0
        max_fit = 0

        self.generate_initial_population()

        self.start_time = time.time()

        while True:
            fbest, xbest = self.best_fit()

            if time.time() - self.start_time > self.time_limit:
                break

            new_pop = np.array([])
            new_pop_fitness = np.array([])
            for i in range(self.pop_size):
                x = self.tournament_selection()
                y = self.tournament_selection()

                new_individual = self.crossover_operator(
                    self.mutate(x),
                    self.mutate(y)
                )
                new_pop = np.append(new_pop, new_individual)
                new_pop_fitness = np.append(new_pop_fitness, self.max_sat_instance.count_sat_clauses(new_individual))

            self.current_pop = new_pop
            self.current_pop_fitness = new_pop_fitness
            generations += 1
            print(fbest)
            if max_fit < fbest:
                max_fit = fbest
        # print('Max Fit: {}'.format(max_fit))
        return generations * self.pop_size, fbest, xbest

    @staticmethod
    def bit_not(bit):
        return '0' if bit == '1' else '1'
