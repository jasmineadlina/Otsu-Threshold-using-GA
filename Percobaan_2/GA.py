import numpy as np
import random
from PIL import Image
from otsu import my_otsu

class GeneticAlgorithm:
    def __init__(self, image, N, max_iterations):
        self.image = np.array(image)
        self.N = N  # Number of individuals in the population
        self.population = self.init_chrome(self.N)
        self.max_iterations = max_iterations  # Maximum number of iterations

    def bin_to_oct(self, chrom):
        return int("".join(map(str, chrom)), 2)

    def init_chrome(self, N):
        return [np.random.randint(0, 2, 8).tolist() for _ in range(N)]

    def get_fitness(self):
        test_nums = [self.bin_to_oct(chrom) for chrom in self.population]
        fitness = [my_otsu(self.image, t) for t in test_nums]
        return fitness

    def select(self):
        fitness = self.get_fitness()
        sum_fitness = np.sum(fitness)
        probability = fitness / sum_fitness
        accu_probability = np.cumsum(probability)
        random_nums = np.random.random(self.N)
        new_population = []
        for num in random_nums:
            for i in range(len(accu_probability)):
                if num < accu_probability[i]:
                    new_population.append(self.population[i])
                    break

        if len(new_population) < self.N:
            new_population.extend(self.init_chrome(self.N - len(new_population)))
        self.population = new_population[:self.N]

    def cross(self):
        for _ in range(self.N // 2):
            if random.random() < 0.7:  # Crossover probability
                idx1, idx2 = random.sample(range(self.N), 2)
                cross_point = random.randint(1, 7)
                self.population[idx1][cross_point:], self.population[idx2][cross_point:] = \
                    self.population[idx2][cross_point:], self.population[idx1][cross_point:]

    def mutate(self):
        for chrom in self.population:
            for i in range(len(chrom)):
                if random.random() < 0.01:  # Mutation probability
                    chrom[i] = 1 - chrom[i]

    def get_threshold(self):
        best_thresholds = []
        best_fitnesses = []
        inter_count = 0
        fitness = self.get_fitness()
        best_fitness = np.max(fitness)
        best_threshold = self.bin_to_oct(self.population[np.argmax(fitness)])
        sustain_count = 0
        cata_count = 0

        while inter_count < self.max_iterations:
            self.select()
            self.cross()
            self.mutate()
            fitness = self.get_fitness()

            max_fitness = np.max(fitness)
            if max_fitness > best_fitness:
                best_fitness = max_fitness
                best_threshold = self.bin_to_oct(self.population[np.argmax(fitness)])
                sustain_count = 0
            else:
                sustain_count += 1

            if sustain_count >= 5:
                max_fitness = np.max(fitness)
                for i in range(len(self.population)):
                    if my_otsu(self.image, self.bin_to_oct(self.population[i])) == max_fitness:
                        self.population[i] = np.random.randint(0, 2, 8).tolist()
                        cata_count += 1
                        if cata_count == 5:
                            sustain_count, cata_count = 0, 0
                            break

            inter_count += 1
            best_thresholds.append(best_threshold)
            best_fitnesses.append(best_fitness)

            print(f"Iteration: {inter_count}")
            print(f"Best Threshold: {best_threshold}")
            print(f"Best Fitness: {best_fitness}")
            print()

        return best_threshold, best_thresholds, best_fitnesses, inter_count
