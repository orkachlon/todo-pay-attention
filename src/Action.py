import random as rd
from typing import Iterable
from datetime import timedelta

import data_io as io
from constants import ActionContexts, ActionTypes

_TYPES = 'types'


class Action:
    """
    Abstract class for any action worth disrupting in my schedule
    """

    username = ''

    def __init__(self, context: ActionContexts, action: str, **kwargs):
        """
        C'tor
        :param subactions: ordered.
        """
        self.contents = dict()
        for action_type in ActionTypes:
            action_type_str = action_type.value
            if action_type_str in kwargs:
                self.contents[action_type_str] = kwargs[action_type_str]
        self.context = context
        self.action = action

    def get_disruptions(self) -> list:
        """
        :return: a list with messages of random disruptions for this action
        """
        alt_action = io.load_alternatives(Action.username,
                                          self.context,
                                          '*' if self.context == ActionContexts.FREE else self.action)
        if not len(alt_action):
            return []
        disruptions = self._disrupt(alt_action, rd.randint(1, len(alt_action[_TYPES])))
        return [self.context_action_message(action_type, disruption)
                for action_type, disruption in disruptions.items()]

    def _disrupt(self, alt_action: dict, num_changes=1) -> dict:
        """
        :param alt_action: alternative action dictionary, contains all possible disruptions for this action.
        :param num_changes: amount of disruptions to get for this action.
        :return: dictionary mapping disruption type to a random disruption, with size num_changes
        """
        action_types = list(alt_action[_TYPES])
        rd.shuffle(action_types)
        disruptions = dict()
        i = 0
        while i < num_changes and i < len(action_types):
            action_type = ActionTypes.from_str(action_types[i])
            contents = alt_action[action_types[i]]

            if action_type == ActionTypes.ORDER:
                disruptions[action_type] = self._disrupt_ordered(contents)
            elif action_type == ActionTypes.ADD:
                disruptions[action_type] = self._disrupt_addable(contents)
            elif action_type == ActionTypes.TIME:
                disruptions[action_type] = self._disrupt_temporal(alt_action)
            elif action_type == ActionTypes.REPLACE:
                disruptions[action_type] = rd.choice(alt_action[ActionTypes.REPLACE.value])

            else:
                print(f"invalid action!:\n{alt_action}")
                return {}
            i += 1
        return disruptions

    def _disrupt_ordered(self, contents: Iterable):
        if ActionTypes.ORDER.value in self.contents:
            contents = self.contents[ActionTypes.ORDER.value]
        rd.shuffle(contents)
        return contents

    def _disrupt_addable(self, contents: Iterable):
        if ActionTypes.ADD.value in self.contents:
            contents = list(filter(lambda x: x not in self.contents[ActionTypes.ADD.value], contents))
        return rd.choice(contents)

    def _disrupt_temporal(self, alt_action: dict):
        action_type_str = ActionTypes.TIME.value
        if action_type_str in self.contents:
            min_time = timedelta(hours=self.contents[action_type_str]['min_time']['hour'],
                                 minutes=self.contents[action_type_str]['min_time']['minute'])
            max_time = timedelta(hours=self.contents[action_type_str]['max_time']['hour'],
                                 minutes=self.contents[action_type_str]['max_time']['minute'])
        else:
            min_time = timedelta(hours=alt_action[action_type_str]['min_time']['hour'],
                                 minutes=alt_action[action_type_str]['min_time']['minute'])
            max_time = timedelta(hours=alt_action[action_type_str]['max_time']['hour'],
                                 minutes=alt_action[action_type_str]['max_time']['minute'])
        delta = max_time - min_time
        return min_time + timedelta(minutes=rd.randint(0, delta.total_seconds() // 600) * 10)

    def _disrupt_replaceable(self):
        pass

    # noinspection DuplicatedCode
    def context_action_message(self, action_type: ActionTypes, disruption):

        if self.context == ActionContexts.FOOD:
            if action_type == ActionTypes.ORDER:
                msg = f"for {self.action}, try this order: "
                for i, item in enumerate(disruption):
                    msg += f"{item} -> " if i < len(disruption) - 1 else f"{item}"
                return msg
            elif action_type == ActionTypes.ADD:
                return f"try adding {disruption} to your {self.action}"
            hours, minutes = _time_str(disruption)
            return f"try eating {self.action} at {hours}:{minutes}"

        if self.context == ActionContexts.HYGIENE:
            if action_type == ActionTypes.ORDER:
                msg = f"for your {self.action}, try this order: "
                for i, item in enumerate(disruption):
                    msg += f"{item} -> " if i < len(disruption) - 1 else f"{item}"
                return msg
            elif action_type == ActionTypes.ADD:
                return f"try adding {disruption} to your {self.action}"
            hours, minutes = _time_str(disruption)
            return f"try doing your {self.action} at {hours}:{minutes}"

        if self.context == ActionContexts.SLEEP:
            if action_type == ActionTypes.TIME:
                hours, minutes = _time_str(disruption)
                return f"try to {self.action} at {hours}:{minutes}"

        if self.context == ActionContexts.GENERAL:
            if action_type == ActionTypes.REPLACE:
                return f"try to {disruption} instead of {self.action}"

        if self.context == ActionContexts.FREE:
            if action_type == ActionTypes.REPLACE:
                return f"try to {disruption} in your free time"
        return f"invalid action: {self.action}"

    def __repr__(self):
        return f"{self.context.value}, {self.action}, {self.contents}"


def _time_str(time: timedelta):
    hours = time.seconds // 3600
    hours = '0' + str(hours) if hours < 10 else str(hours)
    minutes = (time.seconds // 60) % 60
    minutes = '0' + str(minutes) if minutes < 10 else str(minutes)
    return hours, minutes
