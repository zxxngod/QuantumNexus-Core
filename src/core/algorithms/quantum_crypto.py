import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

class QuantumCrypto:
    def __init__(self, num_qubits=1):
        self.num_qubits = num_qubits
        self.qc = QuantumCircuit(num_qubits)
        self.backend = Aer.get_backend('aer_simulator')

    def prepare_qubit(self, state):
        """Prepare a qubit in a specific state."""
        if state == '0':
            self.qc.initialize([1, 0], 0)  # |0>
        elif state == '1':
            self.qc.initialize([0, 1], 0)  # |1>
        elif state == '+':
            self.qc.h(0)  # |+>
        elif state == '-':
            self.qc.h(0)
            self.qc.z(0)  # |->

    def measure_qubit(self):
        """Measure the qubit."""
        self.qc.measure_all()

    def simulate(self):
        """Simulate the quantum circuit."""
        job = execute(self.qc, self.backend, shots=1024)
        result = job.result()
        counts = result.get_counts(self.qc)
        return counts

    def plot_results(self, counts):
        """Plot the results of the measurement."""
        plot_histogram(counts)
        plt.title("Measurement Results")
        plt.show()

    def bb84_protocol(self, alice_bits, basis_choice):
        """Implement the BB84 quantum key distribution protocol."""
        bob_basis = np.random.choice(['Z', 'X'], size=len(alice_bits))
        bob_results = []

        for i in range(len(alice_bits)):
            self.prepare_qubit(alice_bits[i] if basis_choice[i] == 'Z' else ('+' if alice_bits[i] == '0' else '-'))
            self.measure_qubit()
            counts = self.simulate()
            bob_results.append(max(counts, key=counts.get))

        return bob_basis, bob_results

    def sift_key(self, alice_bits, bob_basis, bob_results):
        """Sift the key based on the basis used."""
        key = []
        for i in range(len(alice_bits)):
            if bob_basis[i] == 'Z':
                key.append(bob_results[i])
        return ''.join(key)

    def simulate_noise(self, counts, noise_level=0.1):
        """Simulate quantum noise in the measurement results."""
        noisy_counts = counts.copy()
        for key in counts.keys():
            if np.random.rand() < noise_level:
                # Flip the bit with a certain probability
                noisy_key = '1' if key == '0' else '0'
                noisy_counts[noisy_key] = noisy_counts.get(noisy_key, 0) + counts[key]
                del noisy_counts[key]
        return noisy_counts

if __name__ == "__main__":
    # Example usage of the QuantumCrypto class
    alice_bits = ['0', '1', '0', '1', '1']  # Alice's bits
    basis_choice = np.random.choice(['Z', 'X'], size=len(alice_bits))  # Random basis choice for Alice

    qc = QuantumCrypto()
    bob_basis, bob_results = qc.bb84_protocol(alice_bits, basis_choice)

    # Sift the key
    key = qc.sift_key(alice_bits, bob_basis, bob_results)
    print("Sifted Key:", key)

    # Simulate noise
    counts = qc.simulate()
    noisy_counts = qc.simulate_noise(counts)
    print("Noisy Counts:", noisy_counts)

    # Plot results
    qc.plot_results(counts)
