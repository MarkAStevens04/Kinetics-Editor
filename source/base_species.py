from sympy import symbols

class Species:
    """
    Reactant species
    """
    def __init__(self):
        """
        Initialize self
        """
        self.id = None
        self.value = 0
        self.reactions = []
        self.symbol = None

    def open_json(self, JSON):
        """
        Opens a single json value, unpacks, and sets values
        :param JSON: example: {"id": "A","initial": 100}
        :return: None
        """
        self.value = JSON['initial']
        self.id = JSON['id']
        self.symbol = symbols(JSON['id'])


    def get_id(self):
        return self.id

    def get_symbol(self):
        return self.symbol

    def get_value(self):
        return self.value

    def update_value(self, new_value):
        """
        Updates the value of this species
        :return:
        """
        self.value = new_value