import self as self

from preferences.item import Item
import gc
import operator


class Preferences:
    ''' Preferences class
    This class implements the preferences of each participants.
    '''

    def __init__(self, name):
        self._name = name
        self.criteria_pref = {}
        self.criterias = []
        self.criteria_value = []
        self.items_pref = []
        self.ranking = []
        self.ranking_dict = {}

    def set_criterion_name_list(self, criterion):
        # for criterias in criterion:
        for i, criteria in enumerate(criterion):
            self.criteria_pref[criteria] = (len(criterion) - i)
            self.criterias.append(criteria)

    def add_criterion_value(self, criterion_value):
        self.criteria_value.append(criterion_value.all)
        if criterion_value.all[0] not in self.items_pref:
            self.items_pref.append(criterion_value.all[0])

    def get_score(self):
        for itms in set(self.items_pref):
            score = 0
            for tuple_ in self.criteria_value:
                if itms == tuple_[0]:
                    score += tuple_[2] * self.criteria_pref[tuple_[1]]
                else:
                    score += 0
            self.ranking.append((score, itms))
            self.ranking_dict[itms] = score
            #print(f'{itms} score for {self._name} is:', score)
        self.ranking.sort(key=operator.itemgetter(0), reverse=True)

    def preferred_item(self):
        #a = self.ranking[0,1]
        #print(f'The favorite item for {self._name} is:', self.ranking[0][1])
        return self.ranking[0][1]

    def preferred_between(self, item_1, item_2):
        if self.ranking_dict[item_1] > self.ranking_dict[item_2]:
            return f'{self._name} prefers {item_1} to {item_2}'
        elif self.ranking_dict[item_2] > self.ranking_dict[item_1]:
            return f'{self._name} prefers {item_2} to {item_1}'
        elif self.ranking_dict[item_1] == self.ranking_dict[item_2]:
            return f'{self._name} has no preference between {item_1} and {item_2}'
