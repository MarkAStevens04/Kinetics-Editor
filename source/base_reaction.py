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

    def add_parameter(self, param):
        """
        Adds a parameter to this object's internal storage of parameters
        :param param: Parameter in this reaction
        :return: None
        """
        param_id = param.get_id()
        self.params[param_id] = param

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

        for param_id in json['Parameters']:

            # Get the relevant Parameter from our simulation
            parameter_object = simulation.get_parameter(param_id)

            # Adds parameter object to internal parameter storage
            self.add_parameter(parameter_object)


        # ========== 3. ==========
        # Update our rate law
        rate_string = json['rate_law']

        self.interpret_rate_law(rate_string)





