import os
import pandas as pd
import json as js
from pandas import DataFrame
from datetime import date, timedelta

from constants import ActionContexts


_DATA_PATH = '../data'
_ALTERNATIVES = 'alternatives'
_SCHEDULES = 'schedules'
_CSV = '.csv'
_JSON = '.json'


def _relpath(filename: str) -> str:
    """
    :param filename: name of file from the data folder
    :return: relative path to filename
    """
    return os.path.join(_DATA_PATH, filename)


def _str_to_datetime(date_str: str):
    if len(date_str):
        return date(int('20' + date_str[-2:]), int(date_str[2: -2]), int(date_str[: 2]))
    return None


def _str_to_timedelta(time: str):
    if len(time):
        return timedelta(hours=int(time[: 2]), minutes=int(time[2:]))
    return None


def load_schedule(name: str) -> DataFrame:
    """
    loads the requested schedule from the data folder
    :param name: of schedule
    :return: DataFrame of loaded schedule
    """
    return pd.read_csv(_relpath(os.path.join(_SCHEDULES, name + _CSV)),
                       converters={'date': _str_to_datetime,
                                   'hour': _str_to_timedelta,
                                   'context': str,
                                   'action': str,
                                   'contents': str})


def load_alternatives(username: str, context: ActionContexts, action: str) -> dict:
    """
    Loads the alternative options of given action, from the file of the given context
    :param username: the current user. Used to navigate to the user's alternatives folder.
    :param context: to which the action belongs, also the name of the json file
    :param action: to choose from the context
    :return: dictionary of contents of the chosen action
    """
    path = os.path.join(os.path.join(_ALTERNATIVES, username), context.value + _JSON)
    with open(_relpath(path), 'r') as f:
        context_actions = js.load(f)
    return context_actions[action] if action in context_actions else {}


def load_alt_actions(username: str, context: ActionContexts) -> list:
    """
    :param username: the current user. Used to navigate to the user's alternatives folder.
    :param context: to get action list for
    :return: a list of all alternative actions in given context
    """
    path = os.path.join(os.path.join(_ALTERNATIVES, username), context.value + _JSON)
    with open(_relpath(path), 'r') as f:
        context_actions = js.load(f)
    return list(context_actions.keys())
