from qiskit import QuantumCircuit, Aer, execute

def scaling_example():
    # Create a quantum circuit with multiple qubits
    circuit = QuantumCircuit(3)
    circuit.h(0)  # Apply Hadamard gate to the first qubit
    circuit.cx(0, 1)  # Apply CNOT gate
    circuit.cx(0, 2)  # Apply CNOT gate to the second qubit

    # Execute the circuit
    simulator = Aer.get_backend('aer_simulator')
    result = execute(circuit, simulator).result()
    counts = result.get_counts(circuit)
    return counts

if __name__ == "__main__":
    result = scaling_example()
    print("Scaling result:", result)
