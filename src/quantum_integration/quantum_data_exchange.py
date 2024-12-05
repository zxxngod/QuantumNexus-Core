import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

class QuantumDataExchange:
    def __init__(self):
        self.backend = Aer.get_backend('qasm_simulator')

    def create_entangled_pair(self) -> QuantumCircuit:
        """Create a quantum circuit that generates an entangled pair of qubits."""
        circuit = QuantumCircuit(2, 2)
        circuit.h(0)  # Apply Hadamard gate to the first qubit
        circuit.cx(0, 1)  # Apply CNOT gate to create entanglement
        return circuit

    def prepare_state(self, circuit: QuantumCircuit, state: str) -> QuantumCircuit:
        """Prepare a specific quantum state to be sent."""
        if state == '0':
            pass  # |0> state is already prepared
        elif state == '1':
            circuit.x(0)  # Prepare |1>
        elif state == '+':
            circuit.h(0)  # Prepare |+> state
        elif state == '-':
            circuit.x(0)
            circuit.h(0)  # Prepare |-> state
        else:
            raise ValueError("Unsupported state. Use '0', '1', '+', or '-'.")

        return circuit

    def measure(self, circuit: QuantumCircuit) -> dict:
        """Measure the qubits in the circuit and return the results."""
        circuit.measure([0, 1], [0, 1])  # Measure both qubits
        job = execute(circuit, self.backend, shots=1024)
        result = job.result()
        counts = result.get_counts(circuit)
        return counts

    def run_data_exchange(self, state: str):
        """Run the quantum data exchange protocol."""
        # Step 1: Create entangled pair
        entangled_circuit = self.create_entangled_pair()

        # Step 2: Prepare the state to send
        prepared_circuit = self.prepare_state(entangled_circuit, state)

        # Step 3: Measure the qubits
        measurement_results = self.measure(prepared_circuit)

        return measurement_results

# Example usage
if __name__ == "__main__":
    qde = QuantumDataExchange()
    state_to_send = '1'  # Change this to '0', '1', '+', or '-' to test different states
    results = qde.run_data_exchange(state_to_send)

    print(f"Measurement results for state '{state_to_send}': {results}")

    # Plot the results
    plot_histogram(results)
    plt.title(f'Measurement Results for State: {state_to_send}')
    plt.show()
