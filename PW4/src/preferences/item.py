class Item:
    ''' Item class
    This class implements the objects about which the argumentation will be
    conducted .

    attr :
    name : the name of the item
    description : the description of the item
    '''

    def __init__(self, name, description):
        """
        Creates a new Item .
        """
        self.__name = name
        self.__description = description

    def __str__(self):
        return self.__name

