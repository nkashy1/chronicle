from chronicle import Messenger
from chronicle.responders.scribes import TextScribe

class TestClass(object):
    zero = 0
    
    def successor(self, number):
        return number + 1

test_object = TestClass()
scribe = TextScribe('TextLogging.txt')
messenger = Messenger(test_object, scribe)

messenger.zero
messenger.successor(6)
messenger.successor(-5.37)
