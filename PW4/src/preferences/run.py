from preferences.Value import Value
from preferences.CriterionName import CriterionName
from preferences.item import Item
from preferences.CriterionValue import CriterionValue
from preferences.Preferences import Preferences

Value
CriterionValue
CriterionName
Item
Preferences


agent_pref = Preferences('Agent_1')
agent_pref.set_criterion_name_list([CriterionName.PRODUCTION_COST, CriterionName.ENVIRONMENT_IMPACT,
                                    CriterionName.CONSUMPTION, CriterionName.DURABILITY, CriterionName.NOISE])
diesel_engine = Item("Diesel Engine", "A super cool diesel engine")
agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.PRODUCTION_COST, Value.VERY_GOOD))
agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.CONSUMPTION, Value.GOOD))
agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.DURABILITY, Value.VERY_GOOD))
agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.ENVIRONMENT_IMPACT, Value.VERY_BAD))
agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.NOISE, Value.VERY_BAD))
electric_engine = Item("Electric Engine", "A very quiet engine")
agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.PRODUCTION_COST, Value.BAD))
agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.CONSUMPTION, Value.VERY_BAD))
agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.DURABILITY, Value.GOOD))
agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.ENVIRONMENT_IMPACT, Value.VERY_GOOD))
agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.NOISE, Value.VERY_GOOD))
ICE = Item("ICE", "nice")
agent_pref.add_criterion_value(CriterionValue(ICE, CriterionName.PRODUCTION_COST, Value.OKAY))
agent_pref.add_criterion_value(CriterionValue(ICE, CriterionName.CONSUMPTION, Value.BAD))
agent_pref.add_criterion_value(CriterionValue(ICE, CriterionName.DURABILITY, Value.OKAY))
agent_pref.add_criterion_value(CriterionValue(ICE, CriterionName.ENVIRONMENT_IMPACT, Value.BAD))
agent_pref.add_criterion_value(CriterionValue(ICE, CriterionName.NOISE, Value.VERY_BAD))


