import json

from source.base_species import Species
from source.base_reaction import Reaction

class Simulation:
    def __init__(self):
        self.t_end = 0
        self.dt = 0
        self.method = None
        self.species = {}
        self.reactions = {}

    def initialize_self(self, JSON):
        """
        Initializes the state of the simulation using extract of json
        :param JSON: {"t_end": 100, "dt": 0.1, "method": "Euler"}
        :return: None
        """

        # Initialize parameters using json treating like dict
        self.t_end = JSON['t_end']
        self.dt = JSON['dt']
        self.method = JSON['method']


    def initialize_species(self, JSON):
        """
        Initializes the species and saves to local storage
        :param JSON: JSON format for all the reactants
        :return:
        """
        # For each species given by the JSON...
        for species_json in JSON:

            # Create a new species object
            species_object = Species()

            # Initialize the species object with the JSON
            species_object.open_json(species_json)

            # Get the id of this species
            species_id = species_object.get_id()

            # Check we don't already have this species tracked...
            if species_id in self.species:
                raise ValueError(f'ERROR: Species {species_id} already exists in this simulation!')

            # Save this species object to the Simulation's dictionary
            self.species[species_id] = species_object

    def initialize_reactions(self, JSON):
        """
        Initializes the reactions and saves to local storage
        :param JSON: JSON format for all the reactions
        :return:
        """
        # For each reaction given by the JSON...
        for reaction_json in JSON:

            # Create a new reaction object
            reaction_object = Reaction()

            # Initialize the reaction object with the JSON
            reaction_object.open_json(reaction_json, simulation=self)

            # Get the id of this reaction
            reaction_id = reaction_object.get_id()

            # Check we don't already have this reaction tracked...
            if reaction_id in self.reactions:
                raise ValueError(f'ERROR: Reaction {reaction_id} already exists in this simulation!')

            # Save this reaction object to the Simulation's dictionary
            self.reactions[reaction_id] = reaction_object



    def initialize_simulation(self, JSON):
        """
        Initializes a simulation by opening the provided JSON
        :param JSON: Opens the JSON, opens all species, reactions, and parameters
        :return:
        """
        self.initialize_self(JSON['Simulation'])
        print(f'JSON: {JSON}')

        self.initialize_species(JSON['Species'])

        self.initialize_reactions(JSON['Reactions'])


        print(f'curr t_end: {self.t_end}')



    def open_json(self, path):
        """
        Opens the json from the given path, and initializes the simulation with that json
        :param path:
        :return:
        """

        # Open json with a cursor, save to JSON variable
        with open(path, "r") as f:
            JSON = json.load(f)

        # Call the master JSON opener
        self.initialize_simulation(JSON)


    def get_species(self, species_id):
        """
        Returns the species given by the id
        :param species_id:
        :return:
        """
        return self.species[species_id]



if __name__ == '__main__':
    sim = Simulation()
    sim.open_json('examples/Medium - Invertase digesting sucrose.json')

    print(f'Species:')
    for spec in sim.species:
        print(f'spec: {spec}')

    print()
    print(f'Reactions:')
    for rxn in sim.reactions:
        print(f'rxn: {rxn}')