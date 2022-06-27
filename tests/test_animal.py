import pytest
from src.biosim.animals import *

herbivores = [{'species': 'Herbivore', 'age': 5, 'weight': 20, 'fitness': 0.0},
              {'species': 'Herbivore', 'age': 0, 'weight': 20, 'fitness': 0.0},
              {'species': 'Herbivore', 'age': 10, 'weight': 50, 'fitness': 0.0},
              {'species': 'Herbivore', 'age': 100, 'weight': 200, 'fitness': 0.0}
              ]

carnivores = [{'species': 'Carnivore', 'age': 10, 'weight': 30, 'fitness': 0.0},
              {'species': 'Carnivore', 'age': 0, 'weight': 20, 'fitness': 0.0},
              {'species': 'Carnivore', 'age': 30, 'weight': 80, 'fitness': 0.0},
              {'species': 'Carnivore', 'age': 100, 'weight': 200, 'fitness': 0.0}
              # {'species': 'Herbivore', 'age': -5, 'weight': 20, 'fitness': 0.0}
              ]


@pytest.fixture
def get_herb_params():
    return {
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


@pytest.fixture
def get_carn_params():
    return {
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


@pytest.mark.parametrize("creature", herbivores)
def test_create_herbivore(creature):
    age = creature['age']
    weight = creature['weight']
    beast = Herbivore(creature).get_dict()
    assert beast['age'] == age
    assert beast['weight'] == weight


@pytest.mark.parametrize("creature", carnivores)
def test_create_carnivore(creature):
    age = creature['age']
    weight = creature['weight']
    beast = Carnivore(creature).get_dict()
    assert beast['age'] == age
    assert beast['weight'] == weight


@pytest.mark.parametrize("creature", herbivores)
def test_aging(creature):
    age = creature['age'] + 1
    beast = Animal(creature)
    beast.aging()
    beast_dict = beast.get_dict()
    assert beast_dict['age'] == age


@pytest.mark.parametrize("creature", herbivores)
def test_weight_loss_herbivore(creature, get_herb_params):
    params = get_herb_params
    weight = creature['weight'] - creature['weight'] * params['eta']
    beast = Herbivore(creature)
    beast.weight_loss()
    beast_dict = beast.get_dict()
    assert beast_dict['weight'] == weight


@pytest.mark.parametrize("creature", carnivores)
def test_weight_loss_carnivore(creature, get_carn_params):
    params = get_carn_params
    weight = creature['weight'] - creature['weight'] * params['eta']
    beast = Carnivore(creature)
    beast.weight_loss()
    beast_dict = beast.get_dict()
    assert beast_dict['weight'] == weight


@pytest.mark.parametrize("creature", herbivores)
def test_fitness_herbivore(creature, get_herb_params):
    weight = creature['weight']
    age = creature['age']
    params = get_herb_params
    phi = (1 / (1 + math.e ** (params['phi_age'] * (age - params['a_half'])))) * \
          (1 / (1 + math.e ** (- params['phi_weight'] * (weight - params['w_half']))))

    beast = Herbivore(creature)
    beast.fitness()
    beast_dict = beast.get_dict()
    assert beast_dict['fitness'] == round(phi, 4)


@pytest.mark.parametrize("creature", carnivores)
def test_fitness_carnivore(creature, get_carn_params):
    weight = creature['weight']
    age = creature['age']
    params = get_carn_params
    phi = (1 / (1 + math.e ** (params['phi_age'] * (age - params['a_half'])))) * \
          (1 / (1 + math.e ** (- params['phi_weight'] * (weight - params['w_half']))))

    beast = Carnivore(creature)
    beast.fitness()
    beast_dict = beast.get_dict()
    assert beast_dict['fitness'] == round(phi, 4)


# @pytest.mark.parametrize("creature, conditions", [({'species': 'Herbivore', 'age': 5, 'weight': 20, 'fitness': 0.0},
#                                                    False),
#                                                   ({'species': 'Herbivore', 'age': 10, 'weight': 0, 'fitness': 0.0},
#                                                    True),
#                                                   ({'species': 'Herbivore', 'age': 0, 'weight': 20, 'fitness': 0.0},
#                                                    True),
#                                                   ])
# def test_death_herbivore(creature, conditions):
#     beast = Herbivore(creature)
#     death_value = conditions
#     death_status = beast.death()
#     assert death_status == death_value
#
#
# @pytest.mark.parametrize("creature, conditions", [({'species': 'Carnivore', 'age': 5, 'weight': 20, 'fitness': 0.0},
#                                                    False),
#                                                   ({'species': 'Carnivore', 'age': 10, 'weight': 0, 'fitness': 0.0},
#                                                    True),
#                                                   ({'species': 'Carnivore', 'age': 250, 'weight': 10, 'fitness': 0.0},
#                                                   True)])
# def test_death_herbivore(creature, conditions):
#     beast = Carnivore(creature)
#     death_value = conditions
#     death_status = beast.death()
#     assert death_status == death_value

@pytest.mark.parametrize("creature, conditions", [({'species': 'Herbivore', 'age': 10, 'weight': 30, 'fitness': 0.0},
                                                   True),
                                                  ({'species': 'Herbivore', 'age': 10, 'weight': 0, 'fitness': 0.0},
                                                   False),
                                                  ({'species': 'Herbivore', 'age': 0, 'weight': 20, 'fitness': 0.0},
                                                   False),
                                                  ])
@pytest.mark.parametrize("no_of_animals", [10])
def test_birth_herbivore(creature, conditions, no_of_animals):
    beast = Herbivore(creature)
    birth_value = conditions
    birth_status, child_weight = beast.birth(no_of_animals)
    assert birth_status == birth_value



