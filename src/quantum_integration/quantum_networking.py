import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from typing import List, Tuple

class QuantumKeyDistribution:
    def __init__(self, num_bits: int):
        self.num_bits = num_bits
        self.sender_key = []
        self.receiver_key = []
        self.basis_sender = []
        self.basis_receiver = []
        self.eavesdropper_intercepted = []

    def prepare_qubits(self) -> List[QuantumCircuit]:
        """Prepare qubits in random states based on the sender's basis."""
        circuits = []
        for _ in range(self.num_bits):
            circuit = QuantumCircuit(1, 1)
            # Randomly choose a basis (0: Z-basis, 1: X-basis)
            basis = np.random.choice([0, 1])
            self.basis_sender.append(basis)

            if basis == 0:  # Z-basis
                state = np.random.choice([0, 1])
                if state == 1:
                    circuit.x(0)  # Prepare |1>
            else:  # X-basis
                state = np.random.choice([0, 1])
                if state == 1:
                    circuit.h(0)  # Prepare |+>

            circuits.append(circuit)
            self.sender_key.append(state)
        return circuits

    def measure_qubits(self, circuits: List[QuantumCircuit]) -> List[int]:
        """Measure the qubits in the receiver's basis."""
        results = []
        for circuit in circuits:
            # Randomly choose a basis for measurement
            basis = np.random.choice([0, 1])
            self.basis_receiver.append(basis)

            if basis == 1:  # X-basis
                circuit.h(0)  # Change to X-basis measurement
            circuit.measure(0, 0)

            # Execute the circuit
            job = execute(circuit, Aer.get_backend('qasm_simulator'), shots=1)
            result = job.result()
            counts = result.get_counts(circuit)
            measured_value = int(list(counts.keys())[0])  # Get the measured value
            results.append(measured_value)
        return results

    def generate_shared_key(self, sender_measurements: List[int], receiver_measurements: List[int]) -> Tuple[List[int], List[int]]:
        """Generate the shared key based on matching measurements."""
        for i in range(self.num_bits):
            if self.basis_sender[i] == self.basis_receiver[i]:
                self.receiver_key.append(receiver_measurements[i])
                self.sender_key.append(sender_measurements[i])
        return self.sender_key, self.receiver_key

    def simulate_eavesdropping(self):
        """Simulate an eavesdropper intercepting the qubits."""
        for i in range(self.num_bits):
            # Eavesdropper randomly chooses a basis
            eavesdropper_basis = np.random.choice([0, 1])
            self.eavesdropper_intercepted.append(eavesdropper_basis)

            # If the eavesdropper measures in the same basis, they get the correct value
            if eavesdropper_basis == self.basis_sender[i]:
                self.eavesdropper_intercepted[i] = self.sender_key[i]
            else:
                # If they measure in a different basis, they get a random value
                self.eavesdropper_intercepted[i] = np.random.choice([0, 1])

    def run_qkd(self):
        """Run the BB84 QKD protocol."""
        circuits = self.prepare_qubits()
        receiver_measurements = self.measure_qubits(circuits)
        sender_key, receiver_key = self.generate_shared_key(self.sender_key, receiver_measurements)
        self.simulate_eavesdropping()

        return sender_key, receiver_key, self.eavesdropper_intercepted

# Example usage
if __name__ == "__main__":
    num_bits = 10  # Number of bits to transmit
    qkd = QuantumKeyDistribution(num_bits)
    sender_key, receiver_key, eavesdropper_key = qkd.run_qkd()

    print(f"Sender's key: {sender_key}")
    print(f"Receiver's key: {receiver_key}")
    print(f"Eavesdropper's intercepted key: {eavesdropper_key}")
