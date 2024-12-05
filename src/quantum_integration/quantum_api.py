from flask import Flask, request, jsonify
from qiskit import QuantumCircuit, Aer, execute
import numpy as np

app = Flask(__name__)

class QuantumAPI:
    def __init__(self):
        self.backend = Aer.get_backend('statevector_simulator')

    def create_circuit(self, num_qubits: int) -> QuantumCircuit:
        """Create a new quantum circuit with the specified number of qubits."""
        return QuantumCircuit(num_qubits)

    def apply_gate(self, circuit: QuantumCircuit, gate: str, target_qubits: list):
        """Apply a quantum gate to the specified target qubits."""
        if gate == 'H':
            circuit.h(target_qubits[0])  # Hadamard gate
        elif gate == 'X':
            circuit.x(target_qubits[0])  # Pauli-X gate
        elif gate == 'CX':
            circuit.cx(target_qubits[0], target_qubits[1])  # CNOT gate
        else:
            raise ValueError("Unsupported gate type.")

    def measure(self, circuit: QuantumCircuit) -> np.ndarray:
        """Measure the qubits in the circuit and return the results."""
        circuit.measure_all()  # Measure all qubits
        job = execute(circuit, self.backend)
        result = job.result()
        return result.get_counts(circuit)

quantum_api = QuantumAPI()

@app.route('/create_circuit', methods=['POST'])
def create_circuit():
    """Create a new quantum circuit."""
    data = request.json
    num_qubits = data.get('num_qubits', 1)
    circuit = quantum_api.create_circuit(num_qubits)
    return jsonify({"message": "Circuit created", "num_qubits": num_qubits})

@app.route('/apply_gate', methods=['POST'])
def apply_gate():
    """Apply a quantum gate to the circuit."""
    data = request.json
    gate = data.get('gate')
    target_qubits = data.get('target_qubits', [])
    circuit = quantum_api.create_circuit(len(target_qubits))  # Create a new circuit for simplicity
    quantum_api.apply_gate(circuit, gate, target_qubits)
    return jsonify({"message": f"{gate} gate applied to qubits {target_qubits}"})

@app.route('/measure', methods=['POST'])
def measure():
    """Measure the qubits in the circuit."""
    data = request.json
    num_qubits = data.get('num_qubits', 1)
    circuit = quantum_api.create_circuit(num_qubits)
    # Apply a sample gate for demonstration
    quantum_api.apply_gate(circuit, 'H', [0])  # Apply Hadamard to the first qubit
    counts = quantum_api.measure(circuit)
    return jsonify({"measurement_results": counts})

if __name__ == '__main__':
    app.run(debug=True)
