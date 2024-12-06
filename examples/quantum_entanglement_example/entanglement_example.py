# entanglement_example.py

from qiskit import QuantumCircuit, Aer, transpile, execute
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Create a Bell state |Φ+⟩ = (|00⟩ + |11⟩) / √2
def create_bell_state():
    circuit = QuantumCircuit(2)
    circuit.h(0)  # Apply Hadamard gate to the first qubit
    circuit.cx(0, 1)  # Apply CNOT gate with qubit 0 as control and qubit 1 as target
    return circuit

# Main function to run the example
def main():
    # Create the Bell state circuit
    bell_circuit = create_bell_state()
    bell_circuit.measure_all()  # Measure all qubits

    # Execute the circuit on a simulator
    backend = Aer.get_backend('aer_simulator')
    transpiled_circuit = transpile(bell_circuit, backend)
    job = execute(transpiled_circuit, backend, shots=1024)
    result = job.result()

    # Get the counts and plot the results
    counts = result.get_counts(bell_circuit)
    print("Counts:", counts)
    plot_histogram(counts)
    plt.title("Measurement Results of Bell State")
    plt.show()

if __name__ == "__main__":
    main()
