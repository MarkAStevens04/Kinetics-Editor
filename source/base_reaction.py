from sympy import symbols, lambdify
from sympy.parsing.sympy_parser import parse_expr

class Reaction:
    def __init__(self):
        """
        Initializes a reaction
        """
        self.id = None
        self.reactants = {}
        self.products = {}
        self.rate_law = None
        self.params = {}

    def add_reactant(self, reactant):
        """
        Adds a reactant to this object's internal storage of reactants
        :param reactant:
        :return: None
        """
        reactant_id = reactant.get_id()
        self.reactants[reactant_id] = reactant

    def add_product(self, product):
        """
        Adds a product to this object's internal storage of products
        :param product:
        :return: None
        """
        product_id = product.get_id()
        self.products[product_id] = product

    def add_parameters(self, param_dict):
        """
        Adds parameters to this object's internal storage of parameters
        :param param_dict: parameter dictionary ex. {"k1": 100, "k2": 1000}
        :return: None
        """
        for param_id, param_value in param_dict.items():
            self.params[param_id] = (param_value, symbols(param_id))

    def interpret_rate_law(self, rate_string):
        """
        Interprets a string and converts it into a rate law.

        ASSUMES self.reactants and self.products have already been populated
        :param rate_string:
        :return:
        """
        # Benefits of symbolic computation
        # https://docs.sympy.org/latest/tutorials/intro-tutorial/intro.html#what-is-symbolic-computation

        # Something like...
        # from sympy import symbols, lambdify
        # from sympy.parsing.sympy_parser import parse_expr
        #
        # A, B, C = symbols('A B C')
        # expr_str = "A + (B / C)"
        # expr = parse_expr(expr_str, local_dict={"A": A, "B": B, "C": C}
        #
        # f = lambdify((A, B, C), expr)
        # print(f(2, 6, 3)) (result is 4)

        # POSSIBLE ERROR:
        # MAYBE WE SHOULD CREATE A SYMBOL MAPPING OUR SIMULATION INSTEAD??
        # That way our rate laws don't just have to rely on concentrations of our reactants and products

        # Takes a dictionary item ('Invertase', <species object>) and
        # returns a  dictionary item ('Invertase', SymPy symbol for Invertase)
        def get_species_symbols(species_tuple):
            species_id = species_tuple[0]
            species_obj = species_tuple[1]
            return species_id, species_obj.get_symbol()

        # Transforms our self.reactants and self.products into dictionaries mapping their ids to symbols
        reactant_dict = dict(map(get_species_symbols, self.reactants.items()))
        product_dict = dict(map(get_species_symbols, self.products.items()))

        # Takes a dictionary item ('k1', (100, SymPy symbol for k1)) and
        # returns a  dictionary item ('k1', SymPy symbol for k1)
        def get_parameter_symbols(parameter_tuple):
            parameter_id = parameter_tuple[0]
            parameter_symbol = parameter_tuple[1][1]
            return parameter_id, parameter_symbol

        # Transforms our self.params into dictionaries mapping their ids to symbols
        parameter_dict = dict(map(get_parameter_symbols, self.params.items()))

        # Combines our reactant, product, and parameter dictionaries
        symbol_dict = reactant_dict | product_dict | parameter_dict

        # Creates a sympy expression
        expr = parse_expr(rate_string, local_dict=symbol_dict)

        # Save this expression
        self.rate_law = expr

        # species_dict = {species_id: species_obj.get_value() for species_id, species_obj in self.reactants.items()}
        # param_dict = {param_id: param_tup[0] for param_id, param_tup in self.params.items()}
        # print(f'species_dict: {species_dict | param_dict}')
        # print(f'Change: {self.evaluate_rate_law(species_dict | param_dict)}')

        # ToDo:
        # Lowkey don't use the base_reaction to perform calculations.
        # Use the simulation to store these expressions and perform the calculations for you!
        # Make like an `optimized_euler` method that turns all this info into a few, hard-to-interpret numpy arrays
        # that just chug through the simulation super quickly.





    def evaluate_rate_law(self, species_dict):
        """
        Evaluates the rate law
        :param species_dict: Map of species_ids to the values, ex: {"A": 100, "B": 200}
        :return: Dictionary with relative change for each species
        """
        change = self.rate_law.subs(species_dict)
        sub_dict = {species_id: -1 * change for species_id in self.reactants}
        add_dict = {species_id: change for species_id in self.products}
        return sub_dict | add_dict


    def get_id(self):
        return self.id


    def open_json(self, json, simulation):
        """
        Opens the given json and populates initial values
        :param json:
        :param simulation:
        :return:
        """
        self.id = json['id']

        # ========== 1. ==========
        # Populate Reactants and Products

        # For each reactant ID given in the json file...
        for reactant_id in json['Reactants']:

            # Get the relevant reactant object from our simulation
            reactant_object = simulation.get_species(reactant_id)

            # Add this reactant object to our list of reactants
            self.add_reactant(reactant_object)

        # For each product ID given in the json file...
        for product_id in json['Products']:

            # Get the relevant product object from our simulation
            product_object = simulation.get_species(product_id)

            self.add_product(product_object)

        # ========== 2. ==========
        # Populate Parameters

        # Adds parameter object to internal parameter storage
        self.add_parameters(json['Parameters'])


        # ========== 3. ==========
        # Update our rate law
        rate_string = json['rate_law']

        self.interpret_rate_law(rate_string)




