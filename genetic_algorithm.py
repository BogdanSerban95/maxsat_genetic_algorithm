import time
import random
import numpy as np
import matplotlib.pyplot as plt


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
        self.cum_norm_fitness = None
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
            self.compute_cum_norm_fit()

    def best_two_fit(self):
        max_idx = np.argpartition(self.current_pop_fitness, -2)[-2:]
        # max_idx = np.argmax(self.current_pop_fitness)
        return self.current_pop_fitness[max_idx[1]], self.current_pop[max_idx[1]], \
               self.current_pop_fitness[max_idx[0]], \
               self.current_pop[max_idx[0]]

    def mutate(self, bits_x):
        # if random.uniform(0, 1) > 0.9:
        #     return bits_x
        mutation_rate = self.mutation_rate / self.ind_size
        y = ''
        # mutation_rate = 0.5
        for bit in bits_x:
            prob = random.uniform(0, 1)
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

    def fitness_proportional_selection(self):
        prob = random.uniform(0, 1)
        for i in range(self.pop_size):
            if self.cum_norm_fitness[i] > prob:
                return self.current_pop[i]

    def uniform_crossover(self, bits_x, bits_y):
        child = ''
        for i in range(self.ind_size):
            child += bits_x[i] if random.uniform(0, 1) < 0.5 else bits_y[i]
        return child

    def compute_cum_norm_fit(self):
        fit_sum = np.sum(self.current_pop_fitness)
        norm_fit = self.current_pop_fitness / fit_sum
        self.cum_norm_fitness = np.cumsum(norm_fit)

    def run_ga(self):
        t = 0
        fbest = 0
        xbest = ''
        fit = []
        generations = 0

        self.generate_initial_population()
        self.start_time = time.time()

        while True:
            fbest, xbest, second_best_fit, second_best_x = self.best_two_fit()

            if time.time() - self.start_time > self.time_limit:
                break

            if fbest == self.max_sat_instance.num_clauses:
                break

            new_pop = np.array([])
            new_pop_fitness = np.array([])

            new_pop = np.append(new_pop, xbest)
            new_pop = np.append(new_pop, second_best_x)

            new_pop_fitness = np.append(new_pop_fitness, fbest)
            new_pop_fitness = np.append(new_pop_fitness, second_best_fit)

            while len(new_pop) < self.pop_size:
                x = self.tournament_selection()
                y = self.tournament_selection()

                # x = self.fitness_proportional_selection()
                # y = self.fitness_proportional_selection()

                new_individual = self.uniform_crossover(
                    self.mutate(x),
                    self.mutate(y)
                )
                #
                # new_individual = self.mutate(self.uniform_crossover(x, y))

                new_pop = np.append(new_pop, new_individual)
                new_pop_fitness = np.append(new_pop_fitness, self.max_sat_instance.count_sat_clauses(new_individual))
            self.current_pop = new_pop
            self.current_pop_fitness = new_pop_fitness
            self.compute_cum_norm_fit()
            generations += 1
            fit.append(fbest)
            # print(fbest)

        plt.plot(fit)
        plt.show()
        return generations * self.pop_size, fbest, xbest

    @staticmethod
    def bit_not(bit):
        return '0' if bit == '1' else '1'
