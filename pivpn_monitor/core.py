from typing import Optional
from datetime import datetime


class Event():
    """
    Encapsulation of a message from a monitor to an action

    """

    def __init__(self, message: str, data: Optional[dict]=None):
        """
        Create a notification to signal a monitor firing an event

        :param message: str
        :param data: dict
        """

        data = data or dict()

        self.message = message
        self.data = data
        self.as_of = datetime.now()

    def __str__(self):
        return "Event: {}".format(self.message)

    def __repr__(self):
        return "{}('{}', {})".format(self.__class__.__name__,
                                   self.message, self.data)
