# Standard modules
import functools
import inspect
import types

# External modules

# chronicle modules


class Messenger(object):
    _forbidden_attribute_names_ = ['_forbidden_attribute_names_',
                                   '_core_object_',
                                   '_assert_admissible_attribute_',
                                   '_responder_',
                                   '_core_members_',
                                   '_core_methods_',
                                   '_bridge_method_',
                                   '_notify_responder_']
    
    def __init__(self, core_object, responder):
        self._responder_ = responder
        
        self._core_object_ = core_object
        core_object_attributes = dir(core_object)
        self._core_members_ = []
        self._core_methods_ = []
        
        for attribute_name in core_object_attributes:
            if is_nonmagical(attribute_name):
                self._assert_admissible_attribute_(attribute_name)
                attribute = getattr(self._core_object_, attribute_name)
                if inspect.ismethod(attribute):
                    self._core_methods_.append(attribute_name)
                    self._make_messenger_method_(attribute_name, attribute)
                else:
                    self._core_members_.append(attribute_name)
    
    def __getattribute__(self, name):
        if name == '_forbidden_attribute_names_':
            return object.__getattribute__(self, name)
        elif name in self._forbidden_attribute_names_:
            return object.__getattribute__(self, name)
        
        if name in self._core_members_:
            self._notify_responder_(name)
            return self._core_object_.__getattribute__(name)
        else:
            return object.__getattribute__(self, name)
    
    def _assert_admissible_attribute_(self, attribute):
        if attribute in self._forbidden_attribute_names_:
            error_message = 'Core object attribute clashes with Messenger attribute.'
            raise MessengerAttributeError(error_message)
        return True
    
    def _make_messenger_method_(self, method_name, method):
        @functools.wraps(method)
        def messenger_method(self, *args, **kwargs):
            self._notify_responder_(method_name, *args, **kwargs)
            result = method(*args, **kwargs)
            return result
        
        setattr(self, method_name, types.MethodType(messenger_method, self))
    
    def _notify_responder_(self, attribute_name, *args, **kwargs):
        if attribute_name in self._core_members_:
            self._responder_.notify(attribute_name)
        elif attribute_name in self._core_methods_:
            self._responder_.notify(attribute_name, *args, **kwargs)
        else:
            raise MessengerAttributeError('Notification request for unregistered attribute.')


def is_magical(attribute_name):
    dunder = '__'
    if attribute_name.startswith(dunder) and attribute_name.endswith(dunder):
        return True
    return False

def is_nonmagical(attribute_name):
    return not is_magical(attribute_name)


class MessengerAttributeError(AttributeError):
    pass
