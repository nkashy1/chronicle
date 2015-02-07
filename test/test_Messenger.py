# Unit testing framework
import unittest
import mock

# System under test
from chronicle import Messenger

# Standard modules

# External modules

# chronicle modules
from chronicle.messenger import MessengerAttributeError


class MessengerBaseTests(unittest.TestCase):
    def setUp(self):
        self.core_object = self.setup_object()
        self.messenger = Messenger(self.core_object)
    
    def setup_object(self):
        return self.CoreClass()
    
    class CoreClass(object):
        def __init__(self):
            self.attribute = None
            self._private_attribute = None
    
    def test_initialization(self):
        return True
    
    def test_nonmagical_attributes_existence(self):
        core_object_attributes = dir(self.core_object)
        for attribute in core_object_attributes:
            if not self.is_magical(attribute):
                self.assertTrue(hasattr(self.messenger, attribute))
    
    def test_attribute_name_clashes(self):
        for attribute_name in self.messenger._forbidden_attribute_names_:
            clash_object = self.setup_object()
            setattr(clash_object, attribute_name, None)
            self.assertRaises(MessengerAttributeError, Messenger, clash_object)
    
    def is_magical(self, attribute_name):
        dunder = '__'
        if attribute_name.startswith(dunder) and attribute_name.endswith(dunder):
            return True
        return False


class MessengerMemberTests(MessengerBaseTests):
    class CoreClass(object):
        def __init__(self):
            self.member = 0
    
    def test_member_values(self):
        core_object_attributes = dir(self.core_object)
        messenger_attributes = dir(self.messenger)
        for attribute in core_object_attributes:
            if not self.is_magical(attribute):
                core_object_attribute_value = getattr(self.core_object, attribute)
                messenger_attribute_value = getattr(self.messenger, attribute)
                self.assertIs(messenger_attribute_value, core_object_attribute_value)


class MessengerMethodTests(MessengerBaseTests):
    class CoreClass(object):
        def __init__(self):
            self.member = 1
        
        def method(self):
            return 'method'
    
    def test_method_call(self):
        self.assertEqual(self.messenger.method(), self.core_object.method())


if __name__ == '__main__':
    cases = (MessengerBaseTests,
             MessengerMemberTests,
             MessengerMethodTests)
    
    suite = unittest.TestSuite()
    
    for test_case in cases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_case))
        
    unittest.TextTestRunner(verbosity = 2).run(suite)