import random
import operator
from numpy import vectorize
class GeneticAlgo():

    def __init__(self, hash_map, start, steps=2,crossover_prob=0.15,mutation_prob=0.15,population_size=5,iterations=100):
        self.crossover_prob=crossover_prob
        self.mutation_prob=mutation_prob
        self.population_size=population_size
        self.hash_map = hash_map
        self.steps = steps
        self.iterations = iterations
        self.start = start
        self.nodes = [k for k in self.hash_map.keys()] 
        self.nodes.remove(start)
        self.genes = []
        self.epsilon = 1 - 1/self.iterations        
        self.generate_genes = vectorize(self.generate_genes)
        self.evaluate_fitness = vectorize(self.evaluate_fitness)
        self.evolve = vectorize(self.evolve)
        self.prune_genes = vectorize(self.prune_genes)
        self.converge = vectorize(self.converge)

        self.generate_genes()

    def generate_genes(self):
        for i in range(self.population_size):
            gene = [self.start]
            options = [k for k in self.nodes]
            while len(gene) < len(self.nodes) + 1:
                node = random.choice(options)
                current = options.index(node)
                gene.append(node)
                del options[current]
            gene.append(self.start)
            self.genes.append(gene)
            #print(self.genes)
        return self.genes

    def evaluate_fitness(self):
        fitness_scores = []
        for gene in self.genes:
            total_distance = 0
            for index in range(1, len(gene)):
                end_node = gene[index]
                start_node = gene[index - 1]
                try:
                    distance = self.hash_map[start_node][end_node]
                except:
                    distance = self.hash_map[end_node][start_node]
                total_distance += distance
            fitness = 1/total_distance
            fitness_scores.append(fitness)
        return fitness_scores

    def evolve(self):
        index_map = {i: '' for i in range(0, len(self.nodes) - 1)} # CHANGED 1 to 0
        indices = [i for i in range(0, len(self.nodes) - 1)] # CHANGED 1 to 0
        remaining = [n for n in self.nodes]
        cross = (1 - self.epsilon) * self.crossover_prob
        mutate = self.epsilon * self.mutation_prob
        crossed_count = int(cross * len(self.nodes) ) # REMOVED -1
        mutated_count = int((mutate * len(self.nodes) )/2) # REMOVED -1
        for index in range(len(self.nodes)-1):
            gene = self.genes[index]
            for i in range(crossed_count):
                try:
                    gene_index = random.choice(indices)
                    sample = gene[gene_index]
                    if sample in remaining:
                        index_map[gene_index] = sample
                        current = indices.index(gene_index)
                        del indices[current]
                        current = remaining.index(sample)
                        del remaining[current]
                    else:
                        continue
                except:
                    pass
        last_gene = self.genes[-1]
        remaining_nodes = [n for n in last_gene if n in remaining]
        for k, v in index_map.items():
            if v != '' or None:
                continue
            else:
                node = remaining_nodes.pop(0)
                index_map[k] = node
        new_gene = [index_map[i] for i in range(0, len(self.nodes) - 1)] # CHANGED 1 to 0
        new_gene.insert(0, self.start)
        new_gene.append(self.start)
        for i in range(mutated_count):
            choices = [c for c in new_gene if c != self.start]
            start_node = random.choice(choices)
            end_node = random.choice(choices)
            index_start = new_gene.index(start_node)
            index_end = new_gene.index(end_node)
            new_gene[index_start] = end_node
            new_gene[index_end] = start_node
        self.genes.append(new_gene)

    def prune_genes(self):
        for i in range(self.steps):
            self.evolve()
        fitness_scores = self.evaluate_fitness()
        for i in range(self.steps):
            worst_gene_index = fitness_scores.index(min(fitness_scores))
            del fitness_scores[worst_gene_index]
        return max(fitness_scores),self.genes[fitness_scores.index(max(fitness_scores))]

    def converge(self):
        for i in range(self.iterations):
            values = self.prune_genes()
            current_score = values[0]
            current_best_gene = values[1]
            self.epsilon -= 1/self.iterations
            if i % 100 == 0:
                print(f'{int(1/current_score)} hops')

        return current_best_gene