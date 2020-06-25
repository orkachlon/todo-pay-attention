import re
import os
import sys
import pandas as pd
import random as rd
from pandas import DataFrame
from datetime import timedelta, date

import data_io as io
from constants import ActionContexts, ActionTypes
from Action import Action

_NUM_CHANGES = 6
# noinspection PyTypeChecker
_CONTEXTS = list(ActionContexts)
_DROP_COLUMNS = ['date']
_USAGE_MSG = """Usage: {} [<options>]

    -f                    use given schedule file
    -u                    use given user's configuration files"""


def parse_contents(row: pd.Series) -> dict:
    contents = dict()
    if '-' in row.contents:
        contents[ActionTypes.ORDER.value] = re.split(r'-', row.contents)
    elif ';' in row.contents:
        contents[ActionTypes.ADD.value] = re.split(r';', row.contents)
    if not pd.isna(row.hour):
        extra_time = timedelta(minutes=30)
        min_time = row.hour - extra_time
        if min_time.days > 0:
            hour = (min_time.seconds // 3600) + 24
        else:
            hour = min_time.seconds // 3600
        min_time = {'hour': hour, 'minute': (min_time.seconds // 60) % 60}
        max_time = row.hour + extra_time
        if max_time.days > 0:
            hour = (max_time.seconds // 3600) + 24
        else:
            hour = max_time.seconds // 3600
        max_time = {'hour': hour, 'minute': (max_time.seconds // 60) % 60}
        contents[ActionTypes.TIME.value] = {'min_time': min_time, 'max_time': max_time}
    return contents


def init_action(row: pd.Series) -> Action:
    """
    Action factory. Initializes an action object by the given data
    :param row: containing all relevant data for action instantiation
    :return: Action object
    """
    context = ActionContexts.from_str(row.context)
    return Action(context, row.action, **parse_contents(row))


def output(act_to_alt: list) -> None:
    """
    Outputs the final result
    :param act_to_alt: dictionary of subactions and their alternatives
    """
    print("Disruptions for the day:")
    i = 1
    for alt in act_to_alt:
        for msg in alt:
            print(f"\t{i}. {msg}")
            i += 1


def main(filename='') -> None:
    """
    Main driver of the program
    :param filename: schedule file name
    """
    if not len(filename):
        contexts = [c for c in ActionContexts]
        contexts_actions = [(context, action)
                            for context in contexts
                            for action in io.load_alt_actions(Action.username, context)]

        output([Action(c, a).get_disruptions() for c, a in rd.sample(contexts_actions,
                                                                     min(len(contexts_actions),
                                                                         _NUM_CHANGES))])

    else:
        Action.username = re.search(r'[a-zA-Z]+', filename).group()
        df = io.load_schedule(filename)  # type: DataFrame
        general = DataFrame({'context': ActionContexts.GENERAL.value,
                             'action': io.load_alt_actions(Action.username, ActionContexts.GENERAL),
                             'hour': timedelta(),
                             'date': date.today(),
                             'contents': ''})
        df = pd.concat([df, general])
        df.drop(columns=_DROP_COLUMNS, inplace=True)
        df = df.loc[(df.context.isin([c.value for c in _CONTEXTS]))]
        df = df.sample(frac=min(1.0, _NUM_CHANGES / df.shape[0])).reset_index(drop=True)

        contexts_actions = [init_action(row) for i, row in df.iterrows()]
        output([act.get_disruptions() for act in contexts_actions])


if __name__ == '__main__':
    if len(sys.argv) == 3:
        if sys.argv[1] == '-f':
            main(sys.argv[2])
            exit(0)
        elif sys.argv[1] == '-u':
            Action.username = sys.argv[2]
            main()
            exit(0)
    print(_USAGE_MSG.format(os.path.basename(__file__)), file=sys.stderr)
    exit(-1)
