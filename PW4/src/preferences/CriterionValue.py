from preferences.Value import Value
from preferences.CriterionName import CriterionName
from preferences.item import Item


class CriterionValue:
    """ CriterionValue class
    This class implements the Criterion Value
    """

    def __init__(self, obj, criteria, value):
        self.obj = obj._Item__name
        self.criteria = criteria
        self.value = value
        self.all = [self.obj, self.criteria, self.value]

    def __str__(self):
        """
        Adds value to an item for each criteria.
        """
        return self.all
