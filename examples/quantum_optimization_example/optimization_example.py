# optimization_example.py

from qiskit import Aer, QuantumCircuit, transpile
from qiskit.circuit import Parameter
from qiskit.algorithms import VQE
from qiskit.primitives import Sampler
from qiskit.quantum_info import Pauli
from qiskit.opflow import I, Z, X, Y, PauliSumOp
import numpy as np

# Define the Hamiltonian for the optimization problem
def create_hamiltonian():
    # Example: A simple Hamiltonian H = 0.5 * I + 0.5 * Z
    hamiltonian = 0.5 * (I ^ I) + 0.5 * (Z ^ I)
    return PauliSumOp.from_list([('IIZ', 0.5), ('ZII', 0.5)])

# Create a variational ansatz circuit
def create_ansatz(theta):
    circuit = QuantumCircuit(2)
    circuit.rx(theta[0], 0)
    circuit.rx(theta[1], 1)
    circuit.measure_all()
    return circuit

# Main function to run the optimization
def main():
    # Create the Hamiltonian
    hamiltonian = create_hamiltonian()

    # Define the parameters for the ansatz
    theta = [Parameter('θ1'), Parameter('θ2')]
    ansatz = create_ansatz(theta)

    # Set up the VQE algorithm
    backend = Aer.get_backend('aer_simulator')
    sampler = Sampler(backend)
    vqe = VQE(ansatz, optimizer='SLSQP', sampler=sampler)

    # Run the VQE algorithm
    result = vqe.compute_minimum_eigenvalue(hamiltonian)
    
    # Print the results
    print("Optimal parameters:", result.optimal_parameters)
    print("Minimum eigenvalue:", result.eigenvalue)

if __name__ == "__main__":
    main()
