import unittest
from src.quantum_integration import quantum_circuit, quantum_api

class TestQuantumIntegration(unittest.TestCase):

    def test_quantum_circuit(self):
        circuit = quantum_circuit.create_circuit()
        self.assertIsNotNone(circuit)
        self.assertTrue(circuit.is_valid())

    def test_quantum_api(self):
        response = quantum_api.call_api("some_endpoint")
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())

if __name__ == '__main__':
    unittest.main()
