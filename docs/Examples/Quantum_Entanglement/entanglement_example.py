from qiskit import QuantumCircuit, Aer, execute

def create_entangled_pair():
    circuit = QuantumCircuit(2)
    circuit.h(0)  # Apply Hadamard gate
    circuit.cx(0, 1)  # Apply CNOT gate
    return circuit

if __name__ == "__main__":
    circuit = create_entangled_pair()
    simulator = Aer.get_backend('aer_simulator')
    result = execute(circuit, simulator).result()
    counts = result.get_counts(circuit)
    print("Entanglement result:", counts)
