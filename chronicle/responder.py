# Standard modules
import abc

# External modules

# chronicle modules


class Responder(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def register(self, messenger, core_object, core_object_state):
        return None
    
    @abc.abstractmethod
    def notify(self, messenger, notification):
        return None


class ResponderKeyError(Exception):
    pass
