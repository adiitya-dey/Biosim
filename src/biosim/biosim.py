import textwrap
from src.biosim.land import Island
import timeit


class BioSim:

    def __init__(self, island_map, ini_pop=None, seed=1,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_dir=None, img_base=None, img_years=None,
                 log_file=None):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param hist_specs: Specifications for histograms, see below
        :param vis_years: years between visualization updates (if 0, disable graphics)
        :param img_dir: String with path to directory for figures
        :param img_base: String with beginning of file name for figures
        :param img_fmt: String with file type for figures, e.g. ’png’
        :param img_years: years between visualizations saved to files (default: vis_years)
        :param log_file: If given, write animal counts to this file
        If ymax_animals is None, the y-axis limit should be adjusted automatically.
        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
        {’Herbivore’: 50, ’Carnivore’: 20}
        hist_specs is a dictionary with one entry per property for which a histogram shall be shown.
        For each property, a dictionary providing the maximum value and the bin width must be
        given, e.g.,
        {’weight’: {’max’: 80, ’delta’: 2}, ’fitness’: {’max’: 1.0, ’delta’: 0.05}}
        Permitted properties are ’weight’, ’age’, ’fitness’.
        If img_dir is None, no figures are written to file. Filenames are formed as
        f’{os.path.join(img_dir, img_base}_{img_number:05d}.{img_fmt}’
        where img_number are consecutive image numbers starting from 0.
        img_dir and img_base must either be both None or both strings.
        """

        self.current_year = 1
        self.island_map = island_map
        self.ini_pop = ini_pop
        self.seed = seed
        self.vis_years = vis_years

        self.geography = [list(line) for line in self.island_map.splitlines()]
        self.island_map = {}
        for y_ax, x_line in enumerate(self.geography):
            for x_ax, land_type in enumerate(x_line):
                self.island_map[(x_ax + 1, y_ax + 1)] = land_type

        self.habitable_map = {}
        for coordinate in self.island_map:
            if self.island_map[coordinate] != "W":
                self.habitable_map[coordinate] = self.island_map[coordinate]

        self.island = Island(self.habitable_map)
        self.island.insert_pop(self.ini_pop)

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.
        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.
        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """

    def simulate(self, num_years):
        """
        Run simulation while visualizing the result.
        :param num_years: number of years to simulate
        """
        herb_age = []
        herb_weight = []
        herb_fitness = []
        carn_age = []
        carn_weight = []
        carn_fitness = []
        for _ in range(1, num_years + 1):
            print("*" * 10)
            migrate_from_to_dict = {}
            for cell in self.island.cells:
                cell.replant()
                cell.feeding()
                cell.procreation()

                cell_herb_age, cell_herb_weight, cell_herb_fitness, cell_carn_age, cell_carn_weight, cell_carn_fitness \
                    = cell.aging()
                herb_age += cell_herb_age
                herb_weight += cell_herb_weight
                herb_fitness += cell_herb_fitness
                carn_age += cell_carn_age
                carn_weight += cell_carn_weight
                carn_fitness += cell_carn_fitness

                # migrate_from_to_dict[cell.coord].append(cell.migration())
                # print(cell.coord, len(cell.herb_pop))
                # print(migrate_from_to_dict)
            print("Herbivore:")
            print(herb_age)
            print(herb_weight)
            print(herb_fitness)

            print("Carnivore:")
            print(carn_age)
            print(carn_weight)
            print(carn_fitness)

            # for values in migrate_to_dict:
            #     if location == cell.coord in self.island.cells:
            #         pass

    def add_population(self, population):
        """
        Add a population to the island
        :param population: List of dictionaries specifying population
        """

    @property
    def year(self):
        """Last year simulated."""

    @property
    def num_animals(self):
        """Total number of animals on island."""

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""


if __name__ == '__main__':
    geography = """\
    WWW
    WLW
    WWW"""

    geogr = textwrap.dedent(geography)

    ini_herbs = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(6)]}]
    ini_carns = [{'loc': (2, 2), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20} for _ in range(2)]}]

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs+ini_carns)
    sim.simulate(num_years=3)
