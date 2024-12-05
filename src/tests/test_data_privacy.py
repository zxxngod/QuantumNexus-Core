import unittest
from src.core.utils import data_validation

class TestDataPrivacy(unittest.TestCase):

    def test_data_validation(self):
        valid_data = {"name": "Alice", "age": 30}
        self.assertTrue(data_validation.validate(valid_data))

    def test_invalid_data(self):
        invalid_data = {"name": "", "age": -1}
        self.assertFalse(data_validation.validate(invalid_data))

if __name__ == '__main__':
    unittest.main()
