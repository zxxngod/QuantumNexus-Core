import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from qiskit.circuit import Parameter
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from scipy.optimize import minimize

class QuantumOptimization:
    def __init__(self, graph):
        self.graph = graph
        self.num_qubits = len(graph)
        self.backend = Aer.get_backend('aer_simulator')

    def create_qaoa_circuit(self, p, gamma, beta):
        """Create a QAOA circuit for the given parameters."""
        circuit = QuantumCircuit(self.num_qubits)

        # Initialize the qubits to |+>
        circuit.h(range(self.num_qubits))

        # Apply the problem Hamiltonian
        for i in range(len(self.graph)):
            for j in self.graph[i]:
                circuit.cx(i, j)
                circuit.rz(2 * gamma, j)
                circuit.cx(i, j)

        # Apply the mixing Hamiltonian
        for i in range(self.num_qubits):
            circuit.rx(2 * beta, i)

        return circuit

    def objective_function(self, params):
        """Objective function to minimize."""
        gamma, beta = params
        circuit = self.create_qaoa_circuit(1, gamma, beta)
        circuit.measure_all()

        # Execute the circuit
        job = execute(circuit, self.backend, shots=1024)
        result = job.result()
        counts = result.get_counts(circuit)

        # Calculate the cost function (Max-Cut value)
        max_cut_value = self.calculate_max_cut(counts)
        return -max_cut_value  # We minimize the negative value

    def calculate_max_cut(self, counts):
        """Calculate the Max-Cut value from the measurement results."""
        max_cut_value = 0
        total_shots = sum(counts.values())

        for bitstring, count in counts.items():
            cut_value = self.calculate_cut_value(bitstring)
            probability = count / total_shots
            max_cut_value += cut_value * probability

        return max_cut_value

    def calculate_cut_value(self, bitstring):
        """Calculate the cut value for a given bitstring."""
        cut_value = 0
        for i in range(len(bitstring)):
            for j in self.graph[i]:
                if bitstring[i] != bitstring[j]:  # Different partitions
                    cut_value += 1
        return cut_value

    def optimize(self):
        """Optimize the parameters using a classical optimizer."""
        initial_params = np.random.rand(2)  # Random initial parameters for gamma and beta
        result = minimize(self.objective_function, initial_params, method='COBYLA')
        return result

    def plot_results(self, counts):
        """Plot the results of the measurement."""
        plot_histogram(counts)
        plt.title("Measurement Results")
        plt.show()

if __name__ == "__main__":
    # Example usage of the QuantumOptimization class
    # Define a simple graph as an adjacency list
    graph = {
        0: [1, 3],
        1: [0, 2],
        2: [1, 3],
        3: [0, 2]
    }

    qopt = QuantumOptimization(graph)

    # Optimize the parameters
    result = qopt.optimize()
    print("Optimization Result:", result)

    # Create the final circuit with optimized parameters
    optimized_gamma, optimized_beta = result.x
    final_circuit = qopt.create_qaoa_circuit(1, optimized_gamma, optimized_beta)
    final_circuit.measure_all()

    # Execute the final circuit
    job = execute(final_circuit, qopt.backend, shots=1024)
    result = job.result()
    counts = result.get_counts(final_circuit)

    # Plot results
    qopt.plot_results(counts)
