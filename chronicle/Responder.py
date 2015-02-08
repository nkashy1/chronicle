# Standard modules
import abc

# External modules

# chronicle modules


class Responder(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def notify(self, notification):
        return None


class Notification(object):
    pass
