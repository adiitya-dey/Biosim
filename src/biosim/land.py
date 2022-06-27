from src.biosim.animals import Herbivore, Carnivore
import random


class Island:
    """
    The Island class creates a set of cells that represents each coordinate of the island.
    """

    def __init__(self, land_map: dict):
        """
        The Initialize function creates set of cells that represent habitable coordinate of the island.
        param land_map: dict
        """
        self.land_map = land_map
        # Create an empty set of cells to store Land class information.
        self.cells = set()
        for coord in self.land_map:
            if self.land_map[coord] == "L":
                self.cells.add(LowLand(coord))
            elif self.land_map[coord] == "H":
                self.cells.add(HighLand(coord))
            elif self.land_map[coord] == "D":
                self.cells.add(Desert(coord))

    def insert_pop(self, pop: list):
        """
        The Insert_pop function inserts population of animals to desired coordinate on the island.
        param pop: list
        :return:
        """
        location = None
        population = None
        for item in pop:
            location = item['loc']
            population = item['pop']

            # Iterate through all Land Cells to identify the location in which population needs to be inserted.
            for cell in self.cells:
                if cell.coord == location:
                    for animal in population:
                        animal['fitness'] = 0.0
                        if animal['species'] == 'Herbivore':
                            # Create dictionary value of Herbivore and store in herbivore population list in Land Cell.
                            herbivore = Herbivore(animal).get_dict()
                            cell.herb_pop.append(herbivore)
                        elif animal['species'] == 'Carnivore':
                            # Create dictionary value of Carnivore and store in carnivore population list in Land Cell.
                            carnivore = Carnivore(animal).get_dict()
                            cell.carn_pop.append(carnivore)


class Land:
    """
    The Land Class defines basic characteristic of each land or cell.
    """
    f_max = None

    def __init__(self, coord):
        """
        The Initialize function creates a basic land or cell to store animal population.
        param coord: tuple
        """
        self.grass = self.f_max
        self.coord = coord
        self.herb_pop = []
        self.carn_pop = []

    def replant(self):
        """
        The Replant function updates the value of land to max vegetation or max grass at the beginning of year.
        :return:
        """
        self.grass = self.f_max

    def reduce_grass(self, fodder: float):
        """
        The Reduce_grass function reduces the amount of grass based on animal's diet.
        param fodder: float
        :return:
        """
        self.grass -= fodder

    def feeding(self):
        """
        The Feeding function loops through the animal list for feeding them annually.
        :return:
        """
        # Sort the herbivore population in descending order of fitness.
        if len(self.herb_pop) > 1:
            self.herb_pop.sort(key=lambda x: x['fitness'], reverse=True)

        for herb in self.herb_pop:
            # If no grass available in Land Cell break the for loop to avoid feeding rest of the herbivores.
            if self.grass <= 0:
                break
            # Based on grass consumed, update herbivore's weight and fitness, and reduce total grass from Land Cell.
            else:
                grass_consumed, herb['weight'], herb['fitness'] = Herbivore(herb).eat(self.grass)
                self.reduce_grass(grass_consumed)

        # Sort the herbivore population in ascending order of fitness for carnivore consumption.
        if len(self.herb_pop) > 1:
            self.herb_pop.sort(key=lambda x: x['fitness'], reverse=False)

        # Create a copy "hunters" from carnivore population.
        hunters = self.carn_pop.copy()

        # While hunters exists and herbivores are available randomly choose carnivores from hunters to hunt and feed.
        while len(hunters) != 0:
            # Identify the carnivore index number and carnivore randomly chosen from hunters.
            carn_idx = random.choice(range(0, len(hunters)))
            carn = Carnivore(hunters[carn_idx])

            # Update the herbivore population by removing herbivores that have been hunted or eaten by carnivores.
            self.herb_pop = carn.eat(preys=self.herb_pop)

            # Update the carnivore's weight and fitness in the carnivore population and remove from hunters to avoid
            # getting randomly chosen again.
            self.carn_pop[carn_idx] = carn.get_dict()
            hunters.pop(carn_idx)

            # If no herbivores left after eating then break from the loop.
            if len(self.herb_pop) == 0:
                break


    def procreation(self):
        """
        The Procreation function loops through animal list for giving birth to child annually.
        :return:
        """
        child_list = []

        for herb in self.herb_pop:
            animal = Herbivore(herb)
            birth_status, child_weight = animal.birth(len(self.herb_pop))
            # If birth status is True, update the herbivore's weight and fitness.
            # Also create a child herbivore and add to child list.
            if birth_status:
                herb = animal.get_dict()
                child_list.append(Herbivore({'species': 'Herbivore', 'age': 0.0, 'weight': child_weight,
                                             'fitness': 0.0}).get_dict())
        # Add the children to herbivore population.
        self.herb_pop += child_list
        print(self.herb_pop)

        # Empty all the herbivores from the child list to store children of carnivores.
        child_list.clear()

        for carn in self.carn_pop:
            animal = Carnivore(carn)
            birth_status, child_weight = animal.birth(len(self.carn_pop))
            # If birth status is True, update the carnivore's weight and fitness.
            # Also create a child carnivore and add to child list.
            if birth_status:
                carn = animal.get_dict()
                child_list.append(Carnivore({'species': 'Carnivore', 'age': 0.0, 'weight': child_weight,
                                             'fitness': 0.0}).get_dict())
        # Add the children to carnivore population.
        self.carn_pop += child_list

    def aging(self):
        """
        The Aging function loops through animal list to increase age, reduce weight due to loss and check probability
        of death.
        :return:
        """
        # Create empty list to store herbivore and carnivore - age, weight and fitness for plotting histogram.
        herb_age = []
        herb_weight = []
        herb_fitness = []
        carn_age = []
        carn_weight = []
        carn_fitness = []

        # Create empty list to store index numbers of herbivores and carnivores whose death status is True.
        dead_herb_idx = []
        dead_carn_idx = []

        for i, herb in enumerate(self.herb_pop):
            animal = Herbivore(herb)
            animal.aging()
            animal.weight_loss()
            if animal.death():
                dead_herb_idx.append(i)
            else:
                herb = animal.get_dict()
                herb_age.append(herb['age'])
                herb_weight.append(herb['weight'])
                herb_fitness.append(herb['fitness'])

        for i, carn in enumerate(self.carn_pop):
            animal = Carnivore(carn)
            animal.aging()
            animal.weight_loss()
            if animal.death():
                dead_carn_idx.append(i)
            else:
                carn = animal.get_dict()
                carn_age.append(carn['age'])
                carn_weight.append(carn['weight'])
                carn_fitness.append(carn['fitness'])

        for idx in dead_herb_idx:
            self.herb_pop.pop(idx)
        for idx in dead_carn_idx:
            self.carn_pop.pop(idx)

        return herb_age, herb_weight, herb_fitness, carn_age, carn_weight, carn_fitness

    def migration(self):
        """
        The Migration function loops through animal list to identify animals that need to migrate to another land or
        cell.
        :return:
        """
        migration_list = []
        for herb in self.herb_pop:
            next_loc = herb.migrate(self.coord)
            if next_loc is None:
                continue
            else:
                migration_list.append({next_loc: herb})
        return migration_list


class LowLand(Land):
    """
    The LowLand Class defines characteristics of Lowland type of land or cell.
    """
    f_max = 50.0

    def __init__(self, coord):
        super().__init__(coord)


class HighLand(Land):
    """
        The HighLand Class defines characteristics of Highland type of land or cell.
    """
    f_max = 20.0

    def __init__(self, coord):
        super().__init__(coord)


class Desert(Land):
    """
        The Desert Class defines characteristics of Desert type of land or cell.
    """
    f_max = 0.0

    def __init__(self, coord):
        super().__init__(coord)
