import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.x_wrapper import XWrapper

class TestXWrapper(unittest.TestCase):
    def setUp(self):
        self.wrapper = XWrapper()
    
    def test_guest_token(self):
        self.assertIsNotNone(self.wrapper.guest_token)

if __name__ == '__main__':
    unittest.main()
