from osbrain import Agent
import random
from messages.Messages import Messages
from messages.MessagePerformative import MessagesPerformative


class Manager(Agent):
    """ Manager agent class .
    This class implements the manager agent .

    attr :
    list_items : the list of items to discuss
    selected_items : the list of selected items
    """

    def on_init(self):
        """ Initializes the agent .
        """
        self.engineer_list = []
        self.list_items = []
        self.selected_items = []
        self.log_info(self.name + " initialized")
        self.bind('PUB', alias='main')

    def get_items_list(self, it_list):

        for item in it_list:
            self.list_items.append(item[0])

        """ Initialize communication channel here .
        """

    def send_selected_list(self):
        return self.list_items

    def update_lists(self, item_):
        self.list_items.remove(item_)
        self.selected_items.append(item_)
        return f'The {item_} was added to the selected items list.'

    def get_engineer_list(self, eng_list):
        self.engineer_list = eng_list

    def display(self, message):
        self.log_info("message received: {}".format(message.get_content()))

    def send_msg(self, channel, perf):
        if perf == MessagesPerformative.INFORM_ENG:
            cnt = Messages(self.name, self.engineer_list, perf, self.list_items)
            self.log_info("Message sent: {}".format(cnt.get_infos()))
            self.send(channel, cnt)
        elif perf == MessagesPerformative.QUERY_ITEM:
            cnt = Messages(self.name, self.engineer_list[0], perf, 'Choose an item to discuss')
            self.log_info("Message sent: {}".format(cnt.get_content()))
            self.send(channel, cnt)

        elif perf == MessagesPerformative.QUERY_LIST:
            return Messages(self.name, self.engineer_list[0], perf)