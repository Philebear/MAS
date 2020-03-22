from osbrain import Agent
from preferences.Preferences import Preferences
from preferences.Value import Value
from preferences.CriterionName import CriterionName
from preferences.item import Item
from preferences.CriterionValue import CriterionValue
from agents.Manager import Manager
from messages.Messages import Messages
from messages.MessagePerformative import MessagesPerformative
from arguments.Argument import Arguments


class Inge(Agent):
    """Engineer agent class.
    This class implements the engineer agent.
    """

    def on_init(self):
        """Initializes the agent. """
        self.item_list = []
        self.engineer_list = []
        self.man_list = []
        self.committed = False
        self.selected = 'none'
        self.fav = 'none'
        self.argu = ('none', 'none', 'none')
        self.arg_list = []
        self.list_of_arguments = []
        if self.name == 'ing1':
            self.bind('PUSH', alias='commit1', handler='display')
            self.bind('REP', alias='response_channel', handler='answer')
            self.bind('PUSH', alias='push_channel1', handler='argue')
            self.address = 'push_channel1'
            self.commit = 'commit1'

        elif self.name == 'ing2':
            self.bind('PUSH', alias='commit2', handler='display')
            self.bind('PUSH', alias='push_channel2', handler='argue')
            self.address = 'push_channel2'
            self.commit = 'commit2'
        self.log_info(self.name + " initialized")

    def set_preferences(self):
        if self.name == 'ing1':
            self.agent_pref = Preferences(self.name)
            self.agent_pref.set_criterion_name_list([CriterionName.PRODUCTION_COST,
                                                     CriterionName.CONSUMPTION,
                                                     CriterionName.DURABILITY,
                                                     CriterionName.NOISE,
                                                     CriterionName.ENVIRONMENT_IMPACT])

        elif self.name == 'ing2':
            self.agent_pref = Preferences(self.name)
            self.agent_pref.set_criterion_name_list([CriterionName.PRODUCTION_COST,
                                                     CriterionName.CONSUMPTION,
                                                     CriterionName.DURABILITY,
                                                     CriterionName.NOISE,
                                                     CriterionName.ENVIRONMENT_IMPACT])

    def set_criteria(self, item, crit, value):
        self.agent_pref.add_criterion_value(CriterionValue(item, crit, value))

    def display(self, message):
        self.log_info("message received: {}".format(message.get_perf_n_content()))
        if message.get_perf() == MessagesPerformative.ASK_WHY:
            self.send_msg('argue_channel', MessagesPerformative.ARGUE)
        elif message.get_perf() == MessagesPerformative.ARGUE:
            self.send_msg('argue_channel', MessagesPerformative.PROPOSE)

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
        if self.agent_pref.ranking[0][1] in self.item_list:
            answer = Messages(self.name, self.man_list[0], MessagesPerformative.QUERY_ITEM,
                              "Chosen item is:" + self.agent_pref.ranking[0][1])
            self.selected = self.agent_pref.ranking[0][1]
            self.fav = self.agent_pref.ranking[0][1]
        else:
            self.selected = self.select_item()
            answer = Messages(self.name, self.man_list[0], MessagesPerformative.QUERY_ITEM,
                              "Chosen item is:" + self.selected)
            self.fav = self.agent_pref.ranking[0][1]
        self.log_info("message sent: {}".format(answer.get_perf_n_content()))
        return answer

    def argue(self, message):
        self.agent_pref.get_score()
        self.log_info("message received: {}".format(message.get_perf_n_content()))

        if message.get_perf() == MessagesPerformative.PROPOSE:
            self.committed = False
            if message.get_content() == self.agent_pref.ranking[0][1]:
                self.fav = self.agent_pref.ranking[0][1]
                self.selected = self.agent_pref.ranking[0][1]
                self.argu = (message.get_content(), 'none', 'none')
                self.send_msg(self.address, MessagesPerformative.ACCEPT, argument=self.argu)
                self.send_msg(self.address, MessagesPerformative.COMMIT)
                self.log_info("message sent: COMMIT {}".format(message.get_content()))
            elif message.get_content() != self.agent_pref.ranking[0][1]:
                self.argu = (message.get_content()[1], 'none', 'none')
                self.selected = message.get_content()
                self.send_msg(self.address, MessagesPerformative.ASK_WHY, argument=self.argu)

        if message.get_perf() == MessagesPerformative.ARGUE:
            if message.get_content()[2] == 'pro':
                res = all(y in self.arg_list for y in self.agent_pref.criterias)
                if not res:
                    for x in self.agent_pref.criteria_value:
                        if x[0] == self.selected:
                            if x[2] == -4:
                                disp = f'{x[1]} is Very Bad'
                                self.argu = (self.selected, disp, 'counter')
                                self.send_msg(self.address, MessagesPerformative.ARGUE, argument=self.argu)
                                break
                            elif x[2] == -2:
                                disp = f'{x[1]} is Bad'
                                self.argu = (self.selected, disp, 'counter')
                                self.send_msg(self.address, MessagesPerformative.ARGUE, argument=self.argu)
                                break
                            elif x[2] == 1:
                                disp = f'{x[1]} is only okay'
                                self.argu = (self.selected, disp, 'counter')
                                self.send_msg(self.address, MessagesPerformative.ARGUE, argument=self.argu)
                                break
                elif res:
                    self.argu = (message.get_content()[1], 'none', 'none')
                    self.send_msg(self.address, MessagesPerformative.ACCEPT, argument=self.argu)
                    self.log_info("message sent: ACCEPT {}".format(message.get_content()[1]))
            elif message.get_content()[2] == 'counter':

                res = all(y in self.arg_list for y in self.agent_pref.criterias)
                if not res:
                    for x in self.agent_pref.criteria_value:
                        if x[0] == self.selected:
                            if x[2] == 4:
                                cont = f'{x[1]} is Very Good'
                                self.argu = (self.selected, cont, 'pro')
                                self.send_msg(self.address, MessagesPerformative.ARGUE, argument=self.argu)
                                break
                            elif x[2] == 2:
                                cont = f'{x[1]} is Good'
                                self.argu = (self.selected, cont, 'pro')
                                self.send_msg(self.address, MessagesPerformative.ARGUE, argument=self.argu)
                                break

                elif res:
                    if self.selected == self.agent_pref.ranking[1][1]:
                        self.selected = self.agent_pref.ranking[2][1]
                        self.send_msg(self.address, MessagesPerformative.PROPOSE)
                        self.log_info("message sent: PROPOSE {}".format(message.get_content()[1]))
                    else:
                        self.selected = self.agent_pref.ranking[1][1]
                        self.send_msg(self.address, MessagesPerformative.PROPOSE)
                        self.log_info("message sent: PROPOSE {}".format(message.get_content()[1]))

        if message.get_perf() == MessagesPerformative.COMMIT:
            if self.committed is False:
                self.committed = True
                self.send_msg(self.address, MessagesPerformative.COMMIT)
                self.send_msg(self.commit, MessagesPerformative.COMMIT)
                self.log_info("message sent: COMMIT MANAGER {}".format(self.selected))
            elif self.committed is True:
                pass

        if message.get_perf() == MessagesPerformative.ASK_WHY:
            self.send_msg(self.address, MessagesPerformative.ARGUE)
            # self.log_info("message sent: {}".format(answer.get_perf_n_content()))

    def send_msg(self, channel, msg, argument=None):

        if msg == MessagesPerformative.PROPOSE:
            self.committed = False
            if self.selected != 'none':
                cnt = Messages(self.name, self.engineer_list, msg, self.selected)
            else:
                self.fav = self.agent_pref.ranking[0][1]
                cnt = Messages(self.name, self.engineer_list, msg, self.fav)
            self.log_info("Message sent: {}".format(cnt.get_perf_n_content()))
            self.send(channel, cnt)

        if msg == MessagesPerformative.INFORM_ENG:
            cnt = Messages(self.name, self.engineer_list, msg, self.list_items)
            self.log_info("Message sent: {}".format(cnt.get_perf_n_content()))
            self.send(channel, cnt)

        if msg == MessagesPerformative.COMMIT:
            cnt = Messages(self.name, self.engineer_list, msg, self.selected)
            self.log_info("Message sent: {}".format(cnt.get_perf_n_content()))
            self.send(channel, cnt)
        if msg == MessagesPerformative.ASK_WHY:
            cnt = Messages(self.name, self.engineer_list, MessagesPerformative.ASK_WHY, "why? {}".format(self.selected))
            self.log_info("Message sent: {}".format(cnt.get_perf_n_content()))
            self.send(channel, cnt)
        if msg == MessagesPerformative.ACCEPT:
            cnt = Messages(self.name, self.engineer_list, MessagesPerformative.ACCEPT, "Accept {}".format(self.selected))
            self.log_info("Message sent: {}".format(cnt.get_perf_n_content()))
            self.send(channel, cnt)

        if msg == MessagesPerformative.ARGUE:
            if argument:
                if argument[2] == 'counter':
                    res = all(y in self.arg_list for y in self.agent_pref.criterias)
                    if not res:
                        if argument[1] not in self.arg_list:
                            self.arg_list.append(argument[1])
                            cnt = Messages(self.name, self.engineer_list, msg, (argument[0], argument[1], argument[2]))
                            self.log_info("Message sent: {}".format(cnt.get_perf_n_content()))
                            self.send(channel, cnt)
                        else:
                            for x in self.agent_pref.criteria_value:
                                if x[0] == self.selected:
                                    if x[1] not in self.arg_list:
                                        cont = x[1]
                                        if x[2] == -4:
                                            #disp = (cont, 'is Very Bad')
                                            self.arg_list.append(argument[1])
                                            cnt = Messages(self.name, self.engineer_list, msg, (cont, 'is Very Bad', 'counter'))
                                            self.log_info("Message sent: {}".format(cnt.get_perf_n_content()))
                                            self.send(channel, cnt)
                                            break
                                        elif x[2] == -2:
                                            #disp = (cont, 'is Bad')
                                            self.arg_list.append(argument[1])
                                            cnt = Messages(self.name, self.engineer_list, msg, (cont, 'is Bad', 'counter'))
                                            self.log_info("Message sent: {}".format(cnt.get_perf_n_content()))
                                            self.send(channel, cnt)
                                            break
                    elif res:
                        cnt = Messages(self.name, self.engineer_list, MessagesPerformative.ACCEPT, self.selected)
                        self.log_info("Message sent: {}".format(cnt.get_perf_n_content()))
                        self.send(channel, cnt)
                elif argument[2] == 'pro':
                    res = all(y in self.arg_list for y in self.agent_pref.criterias)
                    if not res:
                        if argument[1] not in self.arg_list:
                            self.arg_list.append(argument[1])
                            cnt = Messages(self.name, self.engineer_list, msg, (argument[0], argument[1], argument[2]))
                            self.log_info("Message sent: {}".format(cnt.get_perf_n_content()))
                            self.send(channel, cnt)
                        else:
                            for x in self.agent_pref.criteria_value:
                                if x[0] == self.selected:
                                    if x[1] not in self.arg_list:
                                        cont = x[1]
                                        if x[2] == 4:
                                            #disp = (cont, 'is Very Good')
                                            self.arg_list.append(argument[1])
                                            cnt = Messages(self.name, self.engineer_list, msg, (cont, 'is Very Good', 'pro'))
                                            self.log_info("Message sent: {}".format(cnt.get_perf_n_content()))
                                            self.send(channel, cnt)
                                            break
                                        elif x[2] == 2:
                                            #disp = (cont, 'is Good')
                                            self.arg_list.append(argument[1])
                                            cnt = Messages(self.name, self.engineer_list, msg, (cont, 'is Good', 'pro'))
                                            self.log_info("Message sent: {}".format(cnt.get_perf_n_content()))
                                            self.send(channel, cnt)
                                            break
                    elif res:
                        cnt = Messages(self.name, self.engineer_list, MessagesPerformative.ACCEPT, self.selected)
                        self.log_info("Message sent: {}".format(cnt.get_perf_n_content()))
                        self.send(channel, cnt)
            else:
                for x in self.agent_pref.criteria_value:
                    if x[0] == self.selected:
                        if x[1] not in self.arg_list:
                            cont = x[1]
                            if x[2] == 4:
                                disp = cont + 'is Very Good'
                                self.arg_list.append(cont)
                                cnt = Messages(self.name, self.engineer_list, msg, (self.selected, disp, 'pro'))
                                self.log_info("Message sent: {}".format(cnt.get_perf_n_content()))
                                self.send(channel, cnt)
                                break
                            elif x[2] == 2:
                                disp = cont + 'is Good'
                                self.arg_list.append(cont)
                                cnt = Messages(self.name, self.engineer_list, msg, (self.selected, disp, 'pro'))
                                self.log_info("Message sent: {}".format(cnt.get_perf_n_content()))
                                self.send(channel, cnt)
                                break


