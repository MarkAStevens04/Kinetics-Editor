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

    def open_json(self, json):
        """
        Opens a single json value, unpacks, and sets values
        :param json: example: {"id": "A","initial": 100}
        :return: None
        """
        self.value = json['initial']
        self.id = json['id']
        return None

    def update_value(self, new_value):
        """
        Updates the value of this species
        :return:
        """