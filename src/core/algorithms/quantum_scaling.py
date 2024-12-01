import numpy as np
import matplotlib.pyplot as plt
from qiskit import Aer, QuantumCircuit, transpile, assemble, execute
from qiskit.circuit import Parameter
from qiskit.algorithms import NumPyMinimumEigensolver
from qiskit.primitives import Sampler
from qiskit.circuit.library import QAOA
from qiskit.quantum_info import Statevector

class QuantumScaling:
    def __init__(self, num_qubits=3, p=1):
        self.num_qubits = num_qubits
        self.p = p
        self.backend = Aer.get_backend('aer_simulator')

    def create_qaoa_circuit(self, cost_hamiltonian):
        """Create a QAOA circuit for a given cost Hamiltonian."""
        qaoa = QAOA(cost_hamiltonian, p=self.p)
        return qaoa

    def run_qaoa(self, cost_hamiltonian):
        """Run the QAOA algorithm and return the optimal parameters and minimum eigenvalue."""
        qaoa = self.create_qaoa_circuit(cost_hamiltonian)
        sampler = Sampler(backend=self.backend)
        result = qaoa.compute_minimum_eigenvalue(sampler=sampler)
        return result

    def visualize_results(self, result):
        """Visualize the results of the QAOA run."""
        print("Optimal Parameters:", result.optimal_parameters)
        print("Minimum Eigenvalue:", result.eigenvalue)
        
        # Visualize the statevector
        statevector = Statevector(result.eigenstate)
        plt.figure(figsize=(8, 6))
        plt.bar(range(len(statevector)), np.abs(statevector)**2)
        plt.title("Statevector Probability Distribution")
        plt.xlabel("Basis States")
        plt.ylabel("Probability")
        plt.xticks(range(len(statevector)), [f"|{i}>" for i in range(len(statevector))])
        plt.show()

    def create_cost_hamiltonian(self):
        """Create a simple cost Hamiltonian for demonstration."""
        # Example: A simple cost Hamiltonian for a 3-qubit system
        # This Hamiltonian corresponds to the problem of finding the minimum of a simple function
        h = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                       [0, 1, 0, 0, 0, 0, 0, 0],
                       [0, 0, 1, 0, 0, 0, 0, 0],
                       [0, 0, 0, 1, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 1, 0, 0],
                       [0, 0, 0, 0, 1, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 1, 0],
                       [0, 0, 0, 0, 0, 0, 0, 1]])
        return h

if __name__ == "__main__":
    # Example usage of the QuantumScaling class
    quantum_scaling = QuantumScaling(num_qubits=3, p=1)

    # Create a cost Hamiltonian
    cost_hamiltonian = quantum_scaling.create_cost_hamiltonian()

    # Run QAOA
    result = quantum_scaling.run_qaoa(cost_hamiltonian)

    # Visualize results
    quantum_scaling.visualize_results(result)
