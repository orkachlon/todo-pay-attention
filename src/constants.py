from enum import Enum


class ActionTypes(Enum):
    """
    Enum for different types of subactions. Influences how they can be changed.
    """
    ORDER = 'order'
    ADD = 'add'
    TIME = 'time'
    REPLACE = 'replace'

    @staticmethod
    def from_str(type_as_str: str):
        """
        :param type_as_str: string of the requested type.
        :return: the corresponding enum member.
        """
        return {
            'order': ActionTypes.ORDER,
            'add': ActionTypes.ADD,
            'time': ActionTypes.TIME,
            'replace': ActionTypes.REPLACE
        }[type_as_str]


class ActionContexts(Enum):
    """
    Enum for the available action contexts. Influences what they can be changed to.
    """
    FOOD = 'food'
    HYGIENE = 'hygiene'
    FREE = 'free'
    SLEEP = 'sleep'
    GENERAL = 'general'

    @staticmethod
    def from_str(context_as_str: str):
        """
        :param context_as_str: string of the requested context.
        :return: the corresponding enum member.
        """
        return {
            'food': ActionContexts.FOOD,
            'hygiene': ActionContexts.HYGIENE,
            'free': ActionContexts.FREE,
            'sleep': ActionContexts.SLEEP,
            'general': ActionContexts.GENERAL
        }[context_as_str]
