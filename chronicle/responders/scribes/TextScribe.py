# Standard modules

# External modules

# chronicle modules
from chronicle import Responder
from chronicle.responder import ResponderKeyError


class TextScribe(Responder):
    def __init__(self, file_name_txt):
        self.file_name = file_name_txt
        self.messengers = {}
    
    def register(self, messenger, core_object):
        self.messengers[messenger] = core_object
    
    def notify(self, messenger, notification):
        self.write(messenger, notification)
    
    def write(self, messenger, notification):
        try:
            core_object = self.messengers[messenger]
        except KeyError:
            raise ResponderKeyError('Received notification from unregistered messenger.')
        
        pass