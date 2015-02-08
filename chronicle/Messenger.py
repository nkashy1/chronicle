# Standard modules
import functools
import inspect

# External modules

# chronicle modules


class Messenger(object):
    _forbidden_attribute_names_ = ['_forbidden_attribute_names_',
                                   '_core_object_',
                                   '_assert_admissible_attribute_']
    
    def __init__(self, core_object):
        self._core_object_ = core_object
        core_object_attributes = dir(core_object)
        for attribute in core_object_attributes:
            if is_nonmagical(attribute):
                self._assert_admissible_attribute_(attribute)
    
    def __getattribute__(self, name):
        if name == '_forbidden_attribute_names_':
            return object.__getattribute__(self, name)
        elif name in self._forbidden_attribute_names_:
            return object.__getattribute__(self, name)
        return self._core_object_.__getattribute__(name)
    
    def _assert_admissible_attribute_(self, attribute):
        if attribute in self._forbidden_attribute_names_:
            error_message = 'Core object attribute clashes with Messenger attribute.'
            raise MessengerAttributeError(error_message)
        return True


def is_magical(attribute_name):
    dunder = '__'
    if attribute_name.startswith(dunder) and attribute_name.endswith(dunder):
        return True
    return False

def is_nonmagical(attribute_name):
    return not is_magical(attribute_name)


class MessengerAttributeError(AttributeError):
    pass
