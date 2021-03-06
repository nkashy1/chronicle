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
        self.responder = self.setup_responder()
        self.messenger = Messenger(self.core_object, self.responder)
    
    def setup_object(self):
        return self.CoreClass()
    
    def setup_responder(self):
        responder = mock.Mock()
        return responder
    
    class CoreClass(object):
        def __init__(self):
            self.attribute = None
            self._private_attribute = None
    
    def test_initialization(self):
        state = {}
        for member in self.messenger._core_members_:
            state[member] = getattr(self.core_object, member)
        self.responder.register.assert_called_once_with(self.messenger, self.core_object, state)
    
    def test_nonmagical_attributes_existence(self):
        core_object_attributes = dir(self.core_object)
        for attribute in core_object_attributes:
            if not self.is_magical(attribute):
                self.assertTrue(hasattr(self.messenger, attribute))
    
    def test_attribute_name_clashes(self):
        for attribute_name in self.messenger._forbidden_attribute_names_:
            clash_object = self.setup_object()
            setattr(clash_object, attribute_name, None)
            if not self.is_magical(attribute_name):
                self.assertRaises(MessengerAttributeError, Messenger, clash_object, self.responder)
    
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
        for attribute in core_object_attributes:
            if not self.is_magical(attribute):
                core_object_attribute_value = getattr(self.core_object, attribute)
                messenger_attribute_value = getattr(self.messenger, attribute)
                self.assertIs(messenger_attribute_value, core_object_attribute_value)
    
    def test_increment(self):
        member_value = self.core_object.member
        self.messenger.member = self.messenger.member + 1
        updated_value = self.core_object.member
        self.assertEqual(updated_value, member_value + 1)
    
    def test_member_logging(self):
        core_object_attributes = dir(self.core_object)
        for attribute in core_object_attributes:
            if attribute in self.messenger._core_members_:
                attribute_value = getattr(self.messenger, attribute)
                expected_notification = (attribute, attribute_value, None, None)
                self.responder.notify.assert_called_once_with(self.messenger, expected_notification)


class MessengerMethodTests(MessengerBaseTests):
    class CoreClass(object):
        def __init__(self):
            self.member = 1
        
        def method(self):
            return 'method'
        
        def successor(self, a):
            return a + 1
    
    def test_method_call(self):
        messenger_result = self.messenger.method()
        core_object_result = self.core_object.method()
        self.assertEqual(messenger_result, core_object_result)
        expected_notification = ('method', 'method', (), {})
        self.responder.notify.assert_called_once_with(self.messenger, expected_notification)
    
    def test_successor_call(self):
        argument = 1
        messenger_result = self.messenger.successor(argument)
        core_object_result = self.core_object.successor(argument)
        self.assertEqual(messenger_result, core_object_result)
        expected_notification = ('successor', self.core_object.successor(argument), (argument,), {})
        self.responder.notify.assert_called_once_with(self.messenger, expected_notification)


if __name__ == '__main__':
    cases = (MessengerBaseTests,
             MessengerMemberTests,
             MessengerMethodTests)
    
    suite = unittest.TestSuite()
    
    for test_case in cases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_case))
        
    unittest.TextTestRunner(verbosity = 2).run(suite)