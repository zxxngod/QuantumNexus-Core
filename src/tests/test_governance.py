import unittest
from src.core.governance import voting_mechanism, dao_structure

class TestGovernance(unittest.TestCase):

    def test_voting_mechanism(self):
        votes = {"yes": 10, "no": 5}
        result = voting_mechanism.calculate_result(votes)
        self.assertEqual(result, "yes")

    def test_dao_structure(self):
        dao = dao_structure.create_dao("TestDAO")
        self.assertEqual(dao.name, "TestDAO")
        self.assertIsNotNone(dao.members)

if __name__ == '__main__':
    unittest.main()
