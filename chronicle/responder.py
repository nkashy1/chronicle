# Standard modules
import abc

# External modules

# chronicle modules


class Responder(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def register(self, messenger, core_object):
        return None
    
    @abc.abstractmethod
    def notify(self, messenger, notification):
        return None
