import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble, execute
from qiskit.visualization import plot_histogram
from qiskit.providers.aer import AerSimulator

class QuantumCircuitManager:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.circuit = QuantumCircuit(num_qubits)

    def add_hadamard(self, qubit):
        """Apply Hadamard gate to a specified qubit."""
        self.circuit.h(qubit)

    def add_cnot(self, control_qubit, target_qubit):
        """Apply CNOT gate with control and target qubits."""
        self.circuit.cx(control_qubit, target_qubit)

    def add_rotation(self, qubit, theta):
        """Apply rotation gate around the Y-axis."""
        self.circuit.ry(theta, qubit)

    def measure(self, qubit, classical_bit):
        """Measure a qubit and store the result in a classical bit."""
        self.circuit.measure(qubit, classical_bit)

    def entangle_qubits(self, qubit1, qubit2):
        """Create entanglement between two qubits using Hadamard and CNOT."""
        self.add_hadamard(qubit1)
        self.add_cnot(qubit1, qubit2)

    def run_simulation(self, shots=1024):
        """Run the quantum circuit simulation and return the results."""
        simulator = AerSimulator()
        transpiled_circuit = transpile(self.circuit, simulator)
        qobj = assemble(transpiled_circuit)
        result = execute(transpiled_circuit, simulator, shots=shots).result()
        counts = result.get_counts(self.circuit)
        return counts

    def visualize_circuit(self):
        """Visualize the quantum circuit."""
        return self.circuit.draw('mpl')

    def reset_circuit(self):
        """Reset the quantum circuit for a new run."""
        self.circuit = QuantumCircuit(self.num_qubits)

# Example usage
if __name__ == "__main__":
    num_qubits = 3
    qc_manager = QuantumCircuitManager(num_qubits)

    # Create a Bell state (entangled state)
    qc_manager.entangle_qubits(0, 1)

    # Apply rotation to the first qubit
    qc_manager.add_rotation(0, np.pi / 4)

    # Measure the qubits
    qc_manager.measure(0, 0)
    qc_manager.measure(1, 1)
    qc_manager.measure(2, 2)

    # Run the simulation
    results = qc_manager.run_simulation(shots=1024)
    print("Measurement results:", results)

    # Visualize the circuit
    qc_manager.visualize_circuit()
