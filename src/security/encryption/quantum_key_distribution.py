import numpy as np
import random
import hashlib
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class QuantumKeyDistribution:
    def __init__(self, num_bits):
        self.num_bits = num_bits
        self.alice_bits = []
        self.alice_bases = []
        self.bob_bases = []
        self.shared_key = []
        self.error_rate = 0.0
        self.eavesdropping_detected = False

    def generate_bits_and_bases(self):
        """Alice generates random bits and bases."""
        self.alice_bits = [random.randint(0, 1) for _ in range(self.num_bits)]
        self.alice_bases = [random.randint(0, 1) for _ in range(self.num_bits)]
        logging.info("Alice generated bits and bases.")

    def simulate_quantum_channel(self):
        """Simulate the quantum channel and Bob's measurement."""
        for i in range(self.num_bits):
            bob_base = random.randint(0, 1)
            self.bob_bases.append(bob_base)

            # If Bob's basis matches Alice's, he measures the bit
            if bob_base == self.alice_bases[i]:
                self.shared_key.append(self.alice_bits[i])
            else:
                # If the bases do not match, Bob gets a random bit
                self.shared_key.append(random.randint(0, 1))

        logging.info("Quantum channel simulated.")

    def error_correction(self):
        """Perform error correction by comparing a subset of bits."""
        comparison_bits = int(self.num_bits * 0.1)  # Compare 10% of the bits
        alice_comparison = self.shared_key[:comparison_bits]
        bob_comparison = self.shared_key[:comparison_bits]

        # Simulate a random error in the channel
        errors = sum(1 for a, b in zip(alice_comparison, bob_comparison) if a != b)
        self.error_rate = errors / comparison_bits

        # Eavesdropping detection based on error rate
        if self.error_rate > 0.1:  # 10% error threshold
            self.eavesdropping_detected = True
            logging.warning("Eavesdropping detected! Error rate too high.")
        else:
            logging.info(f"Error rate acceptable: {self.error_rate:.2%}")

    def privacy_amplification(self):
        """Apply privacy amplification to the shared key."""
        if not self.shared_key:
            return

        # Hash the shared key to reduce its length and increase security
        hash_length = len(self.shared_key) // 2
        key_hash = hashlib.sha256(bytes(self.shared_key)).hexdigest()
        self.shared_key = key_hash[:hash_length]
        logging.info("Privacy amplification applied.")

    def get_shared_key(self):
        """Return the final shared key."""
        return self.shared_key

    def run_qkd_protocol(self):
        """Run the complete QKD protocol."""
        self.generate_bits_and_bases()
        self.simulate_quantum_channel()
        self.error_correction()
        self.privacy_amplification()

        if self.eavesdropping_detected:
            logging.info("Key exchange failed due to eavesdropping.")
            return None
        else:
            final_key = self.get_shared_key()
            logging.info("Key exchange successful.")
            return final_key

if __name__ == "__main__":
    num_bits = int(input("Enter the number of bits for key distribution: "))
    qkd = QuantumKeyDistribution(num_bits)

    final_key = qkd.run_qkd_protocol()
    if final_key is not None:
        print("Final shared key:", final_key)
    else:
        print("No secure key could be established due to eavesdropping.")
