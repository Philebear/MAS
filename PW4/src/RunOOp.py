#!/usr/bin/env python3

"""Main file.

The main file running the name server, creating the agents, and playing with them.
"""

from osbrain import run_agent
from osbrain import run_nameserver
from osbrain import Agent
import time

from agents.Manager import Manager
from agents.Engineer import Engineer
from messages.Messages import Messages
from messages.MessagePerformative import MessagesPerformative
from preferences.Value import Value
from preferences.CriterionName import CriterionName
from preferences.item import Item
from preferences.CriterionValue import CriterionValue
from preferences.Preferences import Preferences

if __name__ == '__main__':
    """
    Main program of the PW4 engine. 
    """
    # Init items and preferences

    diesel_engine = Item('Diesel Engine', 'A super cool diesel engine')
    electric_engine = Item('Electric Engine', 'A very quiet engine')
    ICE = Item('ICE', 'A cheap engine')
    items_list = [('Diesel Engine', 'A super cool diesel engine'), ('Electric Engine', 'A very quiet engine'),
                  ('ICE', 'A cheap engine')]
    engineer_list = ['eng1', 'eng2']
    man_list = ['man1']

    # System deployment
    ns = run_nameserver()
    Manager_1 = run_agent('man1', base=Manager)
    Engineer_1 = run_agent('eng1', base=Engineer)
    Engineer_2 = run_agent('eng2', base=Engineer)

    Manager_1.get_items_list(items_list)
    Manager_1.get_engineer_list(engineer_list)
    Engineer_1.get_items_list(items_list)
    Engineer_1.get_engineer_list(engineer_list)
    Engineer_1.get_man_list(man_list)

    Engineer_2.get_items_list(items_list)
    Engineer_2.get_engineer_list(engineer_list)
    Engineer_2.get_man_list(man_list)

    #agent_pref = Preferences(Engineer_1)
    Engineer_1.set_preferences()

    Engineer_1.set_criteria(diesel_engine, CriterionName.CONSUMPTION, Value.GOOD)
    Engineer_1.set_criteria(diesel_engine, CriterionName.DURABILITY, Value.VERY_GOOD)
    Engineer_1.set_criteria(diesel_engine, CriterionName.ENVIRONMENT_IMPACT, Value.VERY_BAD)
    Engineer_1.set_criteria(diesel_engine, CriterionName.NOISE, Value.BAD)
    Engineer_1.set_criteria(diesel_engine, CriterionName.PRODUCTION_COST, Value.GOOD)

    Engineer_1.set_criteria(electric_engine, CriterionName.PRODUCTION_COST, Value.BAD)
    Engineer_1.set_criteria(electric_engine, CriterionName.CONSUMPTION, Value.GOOD)
    Engineer_1.set_criteria(electric_engine, CriterionName.DURABILITY, Value.GOOD)
    Engineer_1.set_criteria(electric_engine, CriterionName.ENVIRONMENT_IMPACT, Value.VERY_GOOD)
    Engineer_1.set_criteria(electric_engine, CriterionName.NOISE, Value.VERY_GOOD)

    Engineer_1.set_criteria(ICE, CriterionName.PRODUCTION_COST, Value.OKAY)
    Engineer_1.set_criteria(ICE, CriterionName.CONSUMPTION, Value.BAD)
    Engineer_1.set_criteria(ICE, CriterionName.DURABILITY, Value.GOOD)
    Engineer_1.set_criteria(ICE, CriterionName.ENVIRONMENT_IMPACT, Value.BAD)
    Engineer_1.set_criteria(ICE, CriterionName.NOISE, Value.VERY_BAD)

    Engineer_2.set_preferences()
    Engineer_2.set_criteria(diesel_engine, CriterionName.CONSUMPTION, Value.GOOD)
    Engineer_2.set_criteria(diesel_engine, CriterionName.DURABILITY, Value.VERY_GOOD)
    Engineer_2.set_criteria(diesel_engine, CriterionName.ENVIRONMENT_IMPACT, Value.VERY_BAD)
    Engineer_2.set_criteria(diesel_engine, CriterionName.NOISE, Value.BAD)
    Engineer_2.set_criteria(diesel_engine, CriterionName.PRODUCTION_COST, Value.GOOD)

    Engineer_2.set_criteria(electric_engine, CriterionName.PRODUCTION_COST, Value.BAD)
    Engineer_2.set_criteria(electric_engine, CriterionName.CONSUMPTION, Value.GOOD)
    Engineer_2.set_criteria(electric_engine, CriterionName.DURABILITY, Value.GOOD)
    Engineer_2.set_criteria(electric_engine, CriterionName.ENVIRONMENT_IMPACT, Value.VERY_GOOD)
    Engineer_2.set_criteria(electric_engine, CriterionName.NOISE, Value.VERY_GOOD)

    Engineer_2.set_criteria(ICE, CriterionName.PRODUCTION_COST, Value.OKAY)
    Engineer_2.set_criteria(ICE, CriterionName.CONSUMPTION, Value.BAD)
    Engineer_2.set_criteria(ICE, CriterionName.DURABILITY, Value.GOOD)
    Engineer_2.set_criteria(ICE, CriterionName.ENVIRONMENT_IMPACT, Value.BAD)
    Engineer_2.set_criteria(ICE, CriterionName.NOISE, Value.VERY_BAD)

    # System configuration
    Engineer_1.connect(Manager_1.addr('main'), handler='display')
    Engineer_2.connect(Manager_1.addr('main'), handler='display')

    Manager_1.connect(Engineer_1.addr('response_channel'), alias="response_channel")
    Engineer_1.connect(Engineer_2.addr('argue_channel'), alias="argue_channel")

    # Send messages
    Manager_1.send_msg('main', MessagesPerformative.INFORM_ENG)

    Manager_1.send_msg('response_channel', MessagesPerformative.QUERY_ITEM)
    Manager_1.display(Manager_1.recv('response_channel'))

    Engineer_1.send_msg('argue_channel', MessagesPerformative.PROPOSE)
    Engineer_1.display(Engineer_1.recv('argue_channel'))
    #Engineer_1.send_msg('argue_channel', MessagesPerformative.PROPOSE)

    ns.shutdown()