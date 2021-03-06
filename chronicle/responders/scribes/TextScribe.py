# Standard modules
import datetime

# External modules

# chronicle modules
from chronicle import Responder
from chronicle.responder import ResponderKeyError


class TextScribe(Responder):
    def __init__(self, file_name_txt):
        self.file_name = file_name_txt
        self.messengers = {}
    
    def register(self, messenger, core_object, core_object_state):
        time_now = datetime.datetime.utcnow()
        self.messengers[messenger] = core_object
        self.write_registration(messenger, core_object, core_object_state, time_now)
    
    def notify(self, messenger, notification):
        time_now = datetime.datetime.utcnow()
        self.write_notification(messenger, notification, time_now)
    
    def write_registration(self, messenger, core_object, core_object_state, registration_time):
        state = ','.join(['{0}={1}'.format(member, core_object_state[member]) for member in core_object_state])
        log_string = '---\nREGISTRATION:\nMessenger: {0}\nObject: {1}\nState: {2}\nRegistration time: {3}\n'.format(messenger, core_object, state, registration_time)
        with open(self.file_name, 'ab') as txt:
            txt.write(log_string)
    
    def write_notification(self, messenger, notification, notification_time):
        try:
            core_object = self.messengers[messenger]
        except KeyError:
            raise ResponderKeyError('Received notification from unregistered messenger.')
        
        attribute_name = notification[0]
        return_value = notification[1]
        args = notification[2]
        kwargs = notification[3]
        
        access = 'MEMBER'
        if args is not None:
            access = 'METHOD, ARGS: {0}, KEYWORD ARGS: {1}'.format(args, kwargs)
        
        attribute_string = 'Attribute: {0}\nAccess: {1}\nReturn: {2}'.format(attribute_name, access, return_value)
        
        log_string = '---\nMessenger: {0}\nObject: {1}\n{2}\nTime of notification: {3}\n'.format(messenger, core_object, attribute_string, notification_time)
        
        with open(self.file_name, 'ab') as txt:
            txt.write(log_string)
