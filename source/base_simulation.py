import json

import numpy as np

# May need to change to source.base_species
from base_species import Species
from base_reaction import Reaction

class Simulation:
    def __init__(self):
        self.t_end = 0
        self.dt = 0
        self.method = None
        self.species = {}
        self.reactions = {}

        self.species_map = {}
        self.eqn_list = []

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
    
    def generate_equations(self):
        """
        Generates differential equations for the given species and reactions.
        REQUIRES all reactions and species to already be initialized.
        :returns: Dictionary of IDs to rate laws
        """
        # We must turn our unordered dictionary of items into an ordered list of differential equations.
        # Start by creating an index map which given some species, tells us the index to refer to.
        self.species_map = {}

        # Create an array to store our differential equations.
        self.eqn_list = []

        # Populate our species map and equation list
        for i, species in enumerate(self.species):
            self.species_map[species] = i
            self.eqn_list.append(0)

        # Go through all of our reactions and add their differential equations
        for _, rxn_obj in self.reactions.items():

            curr_rate_law = rxn_obj.rate_law

            # To all of our REACTANTS, subtract the rate law
            for reactant_id in rxn_obj.reactants:

                # Get the index of our species in the equation list
                spec_idx = self.species_map[reactant_id]

                # Subtract this rate from the current species' differential equation
                self.eqn_list[spec_idx] = self.eqn_list[spec_idx] - curr_rate_law

            # To all of our PRODUCTS, add the rate law
            for product_id in rxn_obj.products:

                # Get the index of our species in the equation list
                spec_idx = self.species_map[product_id]

                # Add this rate to the current species' differential equation
                self.eqn_list[spec_idx] = self.eqn_list[spec_idx] + curr_rate_law
            

        print(f'diff eqns: {self.eqn_list}')
        print(f'map: {self.species_map}')


    def solve_via_scipy(self, species_map, eqn_list):
        """
        Solves the IVP given a species map and equation list. 
        """


    def initialize_simulation(self, JSON):
        """
        Initializes a simulation by opening the provided JSON
        :param JSON: Opens the JSON, opens all species, reactions, and parameters
        :return:
        """
        self.initialize_self(JSON['Simulation'])

        self.initialize_species(JSON['Species'])

        self.initialize_reactions(JSON['Reactions'])

        self.generate_equations()


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