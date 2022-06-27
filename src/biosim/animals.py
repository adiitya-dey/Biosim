import math
import random


class Animal:
    """
    The Animal Class defines basic characteristic functions of herbivores and carnivores.
    """
    random.seed(1)
    params = {
        'w_birth': 0.0,
        'sigma_birth': 0.0,
        'beta': 0.0,
        'eta': 0.0,
        'a_half': 0.0,
        'w_half': 0.0,
        'phi_age': 0.0,
        'phi_weight': 0.0,
        'mu': 0.0,
        'gamma': 0.0,
        'zeta': 0.0,
        'xi': 0.0,
        'omega': 0.0,
        'F': 0.0,
        'DeltaPhiMax': 0.0
    }

    def __init__(self, animal: dict):
        """
        Initialization function to define age and weight of animal.
        param animal: dict
        """
        # self.species = animal['species']
        self.phi: float = animal['fitness']
        if animal['age'] < 0.0:
            raise ValueError('Age of an animal cannot be negative. Please enter age greater than 0.')
        else:
            self.age: float = animal['age']
        if animal['weight'] < 0.0:
            raise ValueError('Weight of an animal cannot be zero or negative. Please enter weight of positive real '
                             'number')
        else:
            self.weight: float = animal['weight']

    def aging(self):
        """
        The aging function adds age of animal by 1.
        :return: float
        """
        self.age += 1

    def weight_loss(self):
        """
        The weight_loss function reduces weight of animal by eta * self_weight.
        :return: float
        """
        self.weight -= self.params['eta'] * self.weight

    def fitness(self) -> float:
        """
        The fitness function calculates the phi value of animal which represents its fitness.
        :return: float
        """
        if self.weight <= 0:
            self.phi = 0
        else:
            self.phi = (1 / (1 + math.e ** (self.params['phi_age'] * (self.age - self.params['a_half'])))) * \
                       (1 / (1 + math.e ** (- self.params['phi_weight'] * (self.weight - self.params['w_half']))))
        return self.phi

    def get_dict(self) -> dict:
        return {'age': self.age,
                'weight': round(self.weight, 4),
                'fitness': round(self.fitness(), 4)
                }

    def death(self) -> bool:
        """
        The death function calculates the probability of an animal dying.
        :return: bool
        """
        self.fitness()
        if self.weight <= 0:
            return True

        if random.random() < self.params['omega'] * (1 - self.phi):
            return True
        else:
            return False

    def birth(self, no_of_animals):
        """
        The birth function calculates probability of animal's birth.
        param: no_of_animals
        :return: bool, float
        """
        is_birth: bool = False
        child_weight = random.gauss(self.params['w_birth'], self.params['sigma_birth'])
        min_weight = self.params['zeta'] * (self.params['w_birth'] + self.params['sigma_birth'])
        after_birth_weight = self.weight - self.params['xi'] * child_weight

        if self.weight < child_weight or self.weight < min_weight or self.weight < after_birth_weight:
            is_birth = False
        elif random.random() < min(1, self.params['gamma'] * self.phi * (no_of_animals - 1)):
            is_birth = True
            self.weight = after_birth_weight

        return is_birth, child_weight

    def migrate(self) -> bool:
        """
        The migrate function calculates the probability of animal's migration chance.
        :return: bool
        """
        self.fitness()
        if random.random() > self.params['mu'] * self.phi:
            return True
        else:
            return False

    def migrate_loc(self, location: tuple) -> tuple:
        """
        The Migrate_loc function provides randomly chosen coordinates.
        param location: tuple
        :return: tuple
        """
        return random.choice([(location[0] + 1, location[1] + 1), (location[0] - 1, location[1] - 1),
                              (location[0] + 1, location[1] - 1), (location[0] - 1, location[1] + 1)])


class Herbivore(Animal):
    """
    The Herbivore class defines characteristics of a herbivore animal.
    """
    params = {
        'w_birth': 8.0,
        'sigma_birth': 1.5,
        'beta': 0.9,
        'eta': 0.05,
        'a_half': 40.0,
        'w_half': 10.0,
        'phi_age': 0.6,
        'phi_weight': 0.1,
        'mu': 0.25,
        'gamma': 0.2,
        'zeta': 3.5,
        'xi': 1.2,
        'omega': 0.4,
        'F': 10.0,
        'DeltaPhiMax': None
    }

    def __init__(self, animal: dict):
        """
        The Initialize function creates a herbivore with age and weight
        :param animal: dict
        """
        super().__init__(animal)

    def eat(self, fodder: float):
        """
        The Eat function calculates new_weight of animal after eating.
        param fodder: float
        :return: float
        """
        food = self.params['F'] if self.params['F'] < fodder else fodder
        self.weight += food * self.params['beta']
        return food, self.weight, self.fitness()


class Carnivore(Animal):
    params = {
        'w_birth': 6.0,
        'sigma_birth': 1.0,
        'beta': 0.75,
        'eta': 0.125,
        'a_half': 40.0,
        'w_half': 4.0,
        'phi_age': 0.3,
        'phi_weight': 0.4,
        'mu': 0.4,
        'gamma': 0.8,
        'zeta': 3.5,
        'xi': 1.1,
        'omega': 0.8,
        'F': 50.0,
        'DeltaPhiMax': 10.0
    }

    def __init__(self, animal: dict):
        """
        The Initialize function creates a herbivore with age and weight
        param animal: dict
        """
        super().__init__(animal)
        self.max_food = self.params['F']

    def eat(self, preys: list):

        for idx, prey in enumerate(preys):
            food = prey['weight'] if self.max_food > prey['weight'] else self.max_food
            self.weight += self.params['beta'] * food
            self.max_food -= food
            if self.max_food == 0:
                preys = preys[(idx + 1):]
                break

        return preys

