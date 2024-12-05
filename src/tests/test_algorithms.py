import unittest
from unittest.mock import patch
from src.core.algorithms import quantum_crypto, quantum_ml

class TestQuantumAlgorithms(unittest.TestCase):

    @patch('src.core.algorithms.quantum_crypto.some_external_service')
    def test_quantum_encryption(self, mock_service):
        mock_service.return_value = "encrypted_data"
        result = quantum_crypto.encrypt("sensitive_data")
        self.assertEqual(result, "encrypted_data")
        mock_service.assert_called_once_with("sensitive_data")

    def test_quantum_machine_learning(self):
        data = [1, 2, 3, 4, 5]
        model = quantum_ml.train_model(data)
        self.assertIsNotNone(model)
        self.assertTrue(model.is_trained)

if __name__ == '__main__':
    unittest.main()
