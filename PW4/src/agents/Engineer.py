from osbrain import Agent
from preferences.Preferences import Preferences
from preferences.Value import Value
from preferences.CriterionName import CriterionName
from preferences.item import Item
from preferences.CriterionValue import CriterionValue
from agents.Manager import Manager
from messages.Messages import Messages
from messages.MessagePerformative import MessagesPerformative


class Engineer(Agent):
    """Engineer agent class.
    This class implements the engineer agent.
    """

    def on_init(self):
        """Initializes the agent. """
        self.item_list = []
        self.engineer_list = []
        self.man_list = []
        self.selected = 'none'
        self.fav = 'none'
        if self.name == 'eng1':
            self.bind('REP', alias='response_channel', handler='answer')

        elif self.name == 'eng2':
            self.bind('REP', alias='argue_channel', handler='argue')

        self.log_info(self.name + " initialized")

    def set_preferences(self):
        if self.name == 'eng1':
            self.agent_pref = Preferences(self.name)
            self.agent_pref.set_criterion_name_list([CriterionName.PRODUCTION_COST,
                                                     CriterionName.CONSUMPTION,
                                                     CriterionName.DURABILITY,
                                                     CriterionName.NOISE,
                                                     CriterionName.ENVIRONMENT_IMPACT])

        elif self.name == 'eng2':
            self.agent_pref = Preferences(self.name)
            self.agent_pref.set_criterion_name_list([CriterionName.ENVIRONMENT_IMPACT,
                                                     CriterionName.NOISE,
                                                     CriterionName.DURABILITY,
                                                     CriterionName.CONSUMPTION,
                                                     CriterionName.PRODUCTION_COST])

    def set_criteria(self, item, crit, value):
        self.agent_pref.add_criterion_value(CriterionValue(item, crit, value))

    def display(self, message):
        self.log_info("message received: {}".format(message.get_perf_n_content()))
        if message.get_perf() == MessagesPerformative.ASK_WHY:
            self.send_msg('argue_channel', MessagesPerformative.ARGUE)
        elif message.get_perf() == MessagesPerformative.ARGUE:
            self.send_msg('argue_channel', MessagesPerformative.PROPOSE, itm=message.get_content())

    def select_item(self):
        self.agent_pref.get_score()
        ram = []
        for itm in self.item_list:
            ram.append(itm)
        ram.sort()
        choice = ram[0][1]
        return choice

    def get_items_list(self, it_list):

        for item in it_list:
            self.item_list.append(item[0])

    def get_engineer_list(self, eng_list):
        for x in eng_list:
            if x != self.name:
                self.engineer_list.append(x)

    def get_man_list(self, man_list):
        self.man_list = man_list

    def answer(self, message):
        self.agent_pref.get_score()
        self.log_info("message received: {}".format(message.get_perf_n_content()))
        if self.agent_pref.items_pref[0] in self.item_list:
            answer = Messages(self.name, self.man_list[0], MessagesPerformative.QUERY_ITEM,
                              "Chosen item is:" + self.agent_pref.items_pref[0])
            self.selected = self.agent_pref.items_pref[0]
            self.fav = self.agent_pref.items_pref[0]
        else:
            it = self.select_item()
            answer = Messages(self.name, self.man_list[0], MessagesPerformative.QUERY_ITEM,
                              "Chosen item is:" + it)
            self.selected = it
            self.fav = it
        self.log_info("message sent: {}".format(answer.get_perf_n_content()))
        return answer

    def argue(self, message):
        self.agent_pref.get_score()
        self.log_info("message received: {}".format(message.get_perf_n_content()))

        if message.get_perf() == MessagesPerformative.PROPOSE:
            if message.get_content()[1] == self.agent_pref.ranking[0][1]:
                answer = Messages(self.name, self.engineer_list, MessagesPerformative.ACCEPT,
                                  "Accepted {}".format(message.get_content()))
                self.log_info("message sent: {}".format(answer.get_perf_n_content()))
                yield answer
            elif message.get_content() != self.agent_pref.ranking[0][1]:
                self.selected = message.get_content()
                answer = Messages(self.name, self.engineer_list, MessagesPerformative.ASK_WHY,
                                  "why? {}".format(message.get_content()))
                self.log_info("message sent: {}".format(answer.get_perf_n_content()))
                yield answer
        elif message.get_perf() == MessagesPerformative.ARGUE:
            for x in self.agent_pref.criteria_value:
                if x[0] == self.selected:
                    if x[2] == -4:
                        cont = f'{x[1]} is Very Bad'
                    elif x[2] == -2:
                        cont = f'{x[1]} is Bad'
                    elif x[2] == 1:
                        cont = f'{x[1]} is only okay'
            answer = Messages(self.name, self.man_list[0], MessagesPerformative.ARGUE, (self.selected, cont))
            self.log_info("message sent: {}".format(answer.get_perf_n_content()))
            yield answer

    def send_msg(self, channel, msg, itm=None):

        if msg == MessagesPerformative.PROPOSE:
            self.fav = self.agent_pref.ranking[0][1]
            cnt = Messages(self.name, self.engineer_list, msg, self.fav)
            self.log_info("Message sent: {}".format(cnt.get_perf_n_content()))
            self.send(channel, cnt)

        if msg == MessagesPerformative.INFORM_ENG:
            cnt = Messages(self.name, self.engineer_list, msg, self.list_items)
            self.log_info("Message sent: {}".format(cnt.get_perf_n_content()))
            self.send(channel, cnt)

        if msg == MessagesPerformative.ARGUE:
            # if itm ==
            for x in self.agent_pref.criteria_value:
                if x[0] == self.selected:
                    if x[1] in (self.agent_pref.criteria_value[0], self.agent_pref.criteria_value[1],
                                self.agent_pref.criteria_value[2]):
                        if x[2] == 4:
                            cont = f'{x[1]} is Very Good'
                        elif x[2] == 2:
                            cont = f'{x[1]} is Good'
                    elif x[2] == 4:
                        cont = f'{x[1]} is Very Good'
                    elif x[2] == 2:
                        cont = f'{x[1]} is Good'
            cnt = Messages(self.name, self.engineer_list, msg, (self.selected, cont))
            self.log_info("Message sent: {}".format(cnt.get_perf_n_content()))
            self.send(channel, cnt)
