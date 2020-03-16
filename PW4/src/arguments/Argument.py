from preferences.Value import Value
from preferences.CriterionName import CriterionName
from preferences.item import Item
from preferences.CriterionValue import CriterionValue
from preferences.Preferences import Preferences

from messages.Messages import Messages
from messages.MessagePerformative import MessagesPerformative

from agents.Engineer import Engineer


class Arguments:
    """Argument  class.
    This class implements the Message Performative ARGUE.
    """

    def __init__(self, item_name, criterion_value):
        self.itm = item_name
        self.crit_value = criterion_value
        self.arguments = []
