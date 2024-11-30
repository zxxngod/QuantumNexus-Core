from qiskit import QuantumCircuit, Aer, execute

def quantum_optimization_example():
    # Create a simple quantum circuit
    circuit = QuantumCircuit(2)
    circuit.h(0)  # Apply Hadamard gate
    circuit.cx(0, 1)  # Apply CNOT gate

    # Execute the circuit
    simulator = Aer.get_backend('aer_simulator')
    result = execute(circuit, simulator).result()
    counts = result.get_counts(circuit)
    return counts

if __name__ == "__main__":
    result = quantum_optimization_example()
    print("Optimization result:", result)
