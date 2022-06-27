import pytest
from src.biosim.land import *


@pytest.fixture
def create_habitable_island():
    return Island({(1, 1): 'L', (1, 2): 'D', (2, 1): 'H', (2, 2): 'L'})


@pytest.fixture
def lowland_herbivores():
    return [{'loc': (1, 1), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(10)]}]


@pytest.fixture
def lowland_carnivores():
    return [{'loc': (1, 1), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20} for _ in range(10)]}]


@pytest.fixture
def desert_herbivores():
    return [{'loc': (1, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(10)]}]


@pytest.fixture
def desert_carnivores():
    return [{'loc': (1, 2), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20} for _ in range(10)]}]


@pytest.fixture
def highland_herbivores():
    return [{'loc': (2, 1), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(10)]}]


@pytest.fixture
def highland_carnivores():
    return [{'loc': (2, 1), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20} for _ in range(10)]}]


def test_insert_pop(create_habitable_island, lowland_herbivores, lowland_carnivores):
    herb_loc = lowland_herbivores[0]['loc']
    herb_pop = len(lowland_herbivores[0]['pop'])
    carn_loc = lowland_carnivores[0]['loc']
    carn_pop = len(lowland_carnivores[0]['pop'])

    island = create_habitable_island
    island.insert_pop(lowland_herbivores+lowland_carnivores)

    for cell in island.cells:
        if cell.coord == herb_loc:
            assert len(cell.herb_pop) + len(cell.carn_pop) == herb_pop + carn_pop


