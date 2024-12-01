import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_bloch_multivector, plot_histogram

class QuantumEntanglement:
    def __init__(self):
        self.backend = Aer.get_backend('statevector_simulator')

    def create_bell_state(self):
        """Create a Bell state (|Φ⁺⟩ = (|00⟩ + |11⟩) / √2)."""
        circuit = QuantumCircuit(2)

        # Apply a Hadamard gate to the first qubit
        circuit.h(0)

        # Apply a CNOT gate (controlled-X) with the first qubit as control and the second as target
        circuit.cx(0, 1)

        return circuit

    def simulate_circuit(self, circuit):
        """Simulate the quantum circuit and return the state vector."""
        job = execute(circuit, self.backend)
        result = job.result()
        statevector = result.get_statevector(circuit)
        return statevector

    def visualize_entanglement(self, statevector):
        """Visualize the entangled state on the Bloch sphere."""
        # Plot the Bloch sphere representation of the state
        plot_bloch_multivector(statevector)
        plt.title("Bloch Sphere Representation of the Bell State")
        plt.show()

    def measure_state(self, circuit):
        """Measure the state of the qubits."""
        circuit.measure_all()
        job = execute(circuit, self.backend, shots=1024)
        result = job.result()
        counts = result.get_counts(circuit)
        return counts

    def plot_measurement_results(self, counts):
        """Plot the measurement results."""
        plot_histogram(counts)
        plt.title("Measurement Results of the Bell State")
        plt.show()

if __name__ == "__main__":
    # Example usage of the QuantumEntanglement class
    entanglement = QuantumEntanglement()

    # Create a Bell state circuit
    bell_circuit = entanglement.create_bell_state()
    print("Bell State Circuit:")
    print(bell_circuit)

    # Simulate the circuit to get the state vector
    statevector = entanglement.simulate_circuit(bell_circuit)

    # Visualize the entangled state on the Bloch sphere
    entanglement.visualize_entanglement(statevector)

    # Measure the state of the qubits
    bell_circuit.measure_all()
    measurement_counts = entanglement.measure_state(bell_circuit)

    # Plot the measurement results
    entanglement.plot_measurement_results(measurement_counts)
