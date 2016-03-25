from weighted_random import weighted_random_values
from core import get_available_locations, get_tower_types, start
import random


def add_game_values(games):
    with_values = []
    for game in games:
        with_values.append((game, start(game)))

    return with_values


class Genetic:
    def __init__(self):
        self.available_locations = get_available_locations()
        self.tower_types = get_tower_types()

    def mutate(self, game):
        return game

    def build_valid_child(self, towers):
        # TODO fix repeated towers
        return dict(towers)

    def crossover(self, game1, game2):
        child1 = {}
        child2 = {}

        towers = []
        towers.extend(game1.items())
        towers.extend(game2.items())

        random.shuffle(towers)
        half = int(len(towers) / 2)

        child1 = self.build_valid_child(towers[:half])
        child2 = self.build_valid_child(towers[half:])

        return child1, child2

    def random_game(self, towers_size):
        available = list(self.available_locations[:])
        random.shuffle(available)
        positions = [available.pop()
                     for _ in range(towers_size)]
        return {position: random.choice(self.tower_types)
                for position in positions}

    def random_generation(self, population_size, towers_size):
        return [self.random_game(towers_size)
                for _ in range(population_size)]

    def loop(self, initial_games, mutation_factor, n_games,
             max_iterations, save_generations_to=None):

        if save_generations_to:
            self.prepare_generations_file(save_generations_to)

        if n_games % 2 != 0:
            raise Exception("n_games tiene que ser par")

        iterations = 0
        current_games = add_game_values(initial_games)
        while True:
            if save_generations_to:
                self.save_generation(current_games)

            if iterations == max_iterations:
                return current_games

            childs = []
            for _ in range(int(n_games / 2)):
                chosen_parents = weighted_random_values(current_games, 2)
                for child in self.crossover(*chosen_parents):
                    if random.random() <= mutation_factor:
                        child = self.mutate(child)

                    childs.append(child)

            current_games = add_game_values(childs)
            iterations += 1

    def prepare_generations_file(self, generations_file_name):
        self.generations_file = open(generations_file_name, 'w')

    def save_generation(self, games):
        line = repr(games)
        self.generations_file.write(line + '\n')
        self.generations_file.flush()
