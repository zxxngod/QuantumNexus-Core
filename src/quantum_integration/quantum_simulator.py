import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

class QuantumSimulator:
    def __init__(self, num_qubits: int):
        self.num_qubits = num_qubits
        self.state = np.zeros((2 ** num_qubits, 1), dtype=complex)
        self.state[0] = 1  # Initialize to |0...0>

    def apply_gate(self, gate: np.ndarray, target_qubits: List[int]):
        """Apply a quantum gate to the specified target qubits."""
        if not self.is_valid_gate(gate):
            raise ValueError("Invalid gate matrix.")
        
        # Create the full gate matrix for the specified qubits
        full_gate = np.eye(2 ** self.num_qubits, dtype=complex)
        for qubit in target_qubits:
            full_gate = self.tensor_product(full_gate, self.expand_gate(gate, qubit))
        
        # Apply the gate to the current state
        self.state = np.dot(full_gate, self.state)

    def measure(self) -> Tuple[int, float]:
        """Measure the state of the qubits and return the result."""
        probabilities = np.abs(self.state.flatten()) ** 2
        outcome = np.random.choice(range(2 ** self.num_qubits), p=probabilities)
        self.state = np.zeros((2 ** self.num_qubits, 1), dtype=complex)
        self.state[outcome] = 1  # Collapse to the measured state
        return outcome, probabilities[outcome]

    def is_valid_gate(self, gate: np.ndarray) -> bool:
        """Check if the gate is a valid quantum gate."""
        return gate.shape == (2, 2) and np.isclose(np.linalg.norm(gate @ gate.conj().T, ord=1), 1)

    def expand_gate(self, gate: np.ndarray, target_qubit: int) -> np.ndarray:
        """Expand a single qubit gate to act on the full state."""
        identity = np.eye(2, dtype=complex)
        full_gate = identity
        for qubit in range(self.num_qubits):
            if qubit == target_qubit:
                full_gate = np.kron(full_gate, gate)
            else:
                full_gate = np.kron(full_gate, identity)
        return full_gate

    def tensor_product(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """Compute the tensor product of two matrices."""
        return np.kron(a, b)

    def hadamard(self):
        """Apply Hadamard gate to the first qubit."""
        H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
        self.apply_gate(H, [0])

    def pauli_x(self):
        """Apply Pauli-X gate to the first qubit."""
        X = np.array([[0, 1], [1, 0]], dtype=complex)
        self.apply_gate(X, [0])

    def cnot(self, control: int, target: int):
        """Apply CNOT gate with specified control and target qubits."""
        CNOT = np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 0, 1],
                         [0, 0, 1, 0]], dtype=complex)
        self.apply_gate(CNOT, [control, target])

    def visualize_state(self):
        """Visualize the quantum state as a bar chart."""
        probabilities = np.abs(self.state.flatten()) ** 2
        plt.bar(range(2 ** self.num_qubits), probabilities)
        plt.xlabel('State')
        plt.ylabel('Probability')
        plt.title('Quantum State Probabilities')
        plt.xticks(range(2 ** self.num_qubits))
        plt.show()

# Example usage
if __name__ == "__main__":
    simulator = QuantumSimulator(num_qubits=2)
    simulator.hadamard()  # Apply Hadamard to the first qubit
    simulator.cnot(0, 1)  # Apply CNOT with qubit 0 as control and qubit 1 as target
    outcome ```python
    outcome, probability = simulator.measure()  # Measure the state
    print(f"Measured outcome: {outcome}, Probability: {probability}")
    simulator.visualize_state()  # Visualize the state probabilities
