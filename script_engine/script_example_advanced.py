
from custom_components.script_engine.engine import Engine
from custom_components.script_engine.decorator import ToState, Duality, Debug, Arguments, IfState
from custom_components.script_engine.hass.extension import ServiceExt, StateExt, LightExt
from custom_components.script_engine.hass.wrapper import LightWrap
from custom_components.script_engine.const import DOMAIN

from custom_components.script_engine.type.script_time import ScriptTime

import datetime
import random

class _Script_ExampleAdvanced(Engine):

    id = f"{DOMAIN}.playground_id"

    ### Example 1 ###
    ### Stacking conditions 
    ### all three must be fullfilled for function to be called
    @ToState(id="lock.main", state="unlocked")
    @ToState(id="sensor.time", bigger_than=ScriptTime("16:00"))
    @IfState(id="group.family", state="home")
    def _script_example_1(self, *args, **kwargs):
        self.hass.states.async_set(entity_id=self.id, new_state="State_1")

    ### Example 2 ###
    ### Using debug and duality decorators
    ### Duality will fire even if a condition is false, make sure to catch the kwarg "condition"
    @Debug()  # Observe brackets
    @Duality()  # Observe brackets
    @ToState(id="input_boolean.is_home", state="on", debug=False)
    def _script_example_2(self, *args, **kwargs):
        condition = kwargs.get("condition")
        if condition:
            LightExt.turn_on(self.hass, id="light.dining_table", data={})
        else:
            LightExt.turn_off(self.hass, id="light.dining_table", data={})

    ### Example 3 ###
    ### Using a function as a state comparison
    ### Workdays its early, weekend its late
    def dawn():
        now = datetime.datetime.now()
        weekday = now.weekday

        if weekday in [0, 1, 2, 3, 4]:
            return "06:00"
        else:
            return "09:00"

    @ToState(id="sensor.time", state=dawn)
    def _script_example_2(self, *args, **kwargs):
        LightExt.turn_on(self.hass, id="light.hunden_on_off", data={})

    ### Example 4 ###
    ### Using a custom evaluation function
    ### Will turn on the lamp approx one day in five at 15:00 according to a random generator
    def random(new_state: str, old_state: str):
        i = random.random()
        if new_state == "15:00" and i > 0.8:
            return True
        else:
            return False

    @ToState(id="sensor.time", custom_eval=random)
    def _script_example_2(self, *args, **kwargs):
        LightExt.turn_on(self.hass, id="light.kids_room", data={})
