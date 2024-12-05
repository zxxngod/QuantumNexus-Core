import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt
from typing import List, Tuple

class QuantumInteroperability:
    def __init__(self):
        self.backend = Aer.get_backend('statevector_simulator')

    def prepare_state(self, state: str) -> QuantumCircuit:
        """Prepare a quantum circuit for a given state."""
        circuit = QuantumCircuit(1)
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

    def convert_to_bloch(self, statevector: np.ndarray) -> Tuple[float, float, float]:
        """Convert a statevector to Bloch sphere coordinates."""
        theta = 2 * np.arccos(statevector[0])
        phi = np.angle(statevector[1])
        x = np.sin(theta) * np.cos(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(theta)
        return x, y, z

    def measure(self, circuit: QuantumCircuit) -> dict:
        """Measure the qubit in the circuit and return the results."""
        circuit.measure_all()  # Measure all qubits
        job = execute(circuit, self.backend, shots=1024)
        result = job.result()
        counts = result.get_counts(circuit)
        return counts

    def run_interoperability(self, state: str):
        """Run the interoperability protocol."""
        # Step 1: Prepare the quantum state
        circuit = self.prepare_state(state)

        # Step 2: Execute the circuit and get the statevector
        job = execute(circuit, self.backend)
        statevector = job.result().get_statevector(circuit)

        # Step 3: Convert to Bloch sphere coordinates
        bloch_coords = self.convert_to_bloch(statevector)

        # Step 4: Measure the qubit
        measurement_results = self.measure(circuit)

        return statevector, bloch_coords, measurement_results

# Example usage
if __name__ == "__main__":
    qio = QuantumInteroperability()
    state_to_prepare = '+'  # Change this to '0', '1', '+', or '-' to test different states
    statevector, bloch_coords, results = qio.run_interoperability(state_to_prepare)

    print(f"Statevector for state '{state_to_prepare}': {statevector}")
    print(f"Bloch sphere coordinates: {bloch_coords}")
    print(f"Measurement results: {results}")

    # Plot Bloch sphere representation
    plot_bloch_multivector(statevector)
    plt.title(f'Bloch Sphere Representation for State: {state_to_prepare}')
    plt.show()
