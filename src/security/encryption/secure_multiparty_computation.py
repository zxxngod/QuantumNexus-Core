import random
import logging
from hashlib import sha256
from typing import List, Tuple
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ShamirSecretSharing:
    def __init__(self, threshold: int, total_parties: int):
        self.threshold = threshold
        self.total_parties = total_parties
        self.secret = None
        self.shares = []
        self.prime = None

    def _polynomial(self, x: int, coefficients: List[int]) -> int:
        """Evaluate polynomial at x."""
        return sum(coef * (x ** i) for i, coef in enumerate(coefficients)) % self.prime

    def _generate_coefficients(self) -> List[int]:
        """Generate random coefficients for the polynomial."""
        return [random.randint(0, self.prime - 1) for _ in range(self.threshold - 1)]

    def _generate_shares(self) -> List[Tuple[int, int]]:
        """Generate shares for the secret."""
        coefficients = self._generate_coefficients()
        shares = [(i, self._polynomial(i, coefficients)) for i in range(1, self.total_parties + 1)]
        return shares

    def share_secret(self, secret: int) -> List[Tuple[int, int]]:
        """Share the secret among parties."""
        self.secret = secret
        self.prime = self._find_prime_greater_than(secret)
        self.shares = self._generate_shares()
        logging.info("Shares generated successfully.")
        return self.shares

    def reconstruct_secret(self, shares: List[Tuple[int, int]]) -> int:
        """Reconstruct the secret from shares."""
        if len(shares) < self.threshold:
            logging.error("Not enough shares to reconstruct the secret.")
            raise ValueError("Not enough shares to reconstruct the secret.")

        total = 0
        for i, (x_i, y_i) in enumerate(shares):
            numerator = 1
            denominator = 1
            for j, (x_j, _) in enumerate(shares):
                if i != j:
                    numerator = (numerator * (0 - x_j)) % self.prime
                    denominator = (denominator * (x_i - x_j)) % self.prime
            lagrange_coefficient = numerator * pow(denominator, -1, self.prime) % self.prime
            total = (total + y_i * lagrange_coefficient) % self.prime

        logging.info("Secret reconstructed successfully.")
        return total

    def _find_prime_greater_than(self, n: int) -> int:
        """Find a prime number greater than n."""
        def is_prime(num: int) -> bool:
            if num < 2:
                return False
            for i in range(2, int(num**0.5) + 1):
                if num % i == 0:
                    return False
            return True

        prime_candidate = n + 1
        while not is_prime(prime_candidate):
            prime_candidate += 1
        return prime_candidate

class SecureMultipartyComputation:
    def __init__(self, threshold: int, total_parties: int):
        self.shares = []
        self.sss = ShamirSecretSharing(threshold, total_parties)
        self.keys = self._generate_keys(total_parties)

    def _generate_keys(self, total_parties: int) -> List[rsa.RSAPrivateKey]:
        """Generate RSA keys for each party."""
        keys = []
        for _ in range(total_parties):
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            keys.append(private_key)
        return keys

    def encrypt_share(self, share: Tuple[int, int], public_key) -> bytes:
        """Encrypt a share using the public key."""
        encrypted_share = public_key.encrypt(
            str(share).encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_share

    def decrypt_share(self, encrypted_share: bytes, private_key) -> Tuple[int, int]:
        """Decrypt a share using the private key."""
        decrypted_share = private_key.decrypt(
            encrypted_share,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return eval(decrypted_share.decode())

    def share_secret(self, secret: int) -> List[bytes]:
        """Share the secret among parties and encrypt the shares."""
        shares = self.sss.share_secret(secret)
        encrypted_shares = []
        for i, share in enumerate(shares):
            public_key = self.keys[i].public_key()
            encrypted_share = self.encrypt_share(share, public_key)
            encrypted_shares.append(encrypted_share)
        logging.info("Shares encrypted and distributed successfully.")
        return encrypted_shares

    def reconstruct_secret(self, encrypted_shares: List[bytes]) -> int:
        """Reconstruct the secret from encrypted shares."""
        decrypted_shares = []
        for i, encrypted_share in enumerate(encrypted_shares):
            decrypted_share = self.decrypt_share(encrypted_share, self.keys[i])
            decrypted_shares.append(decrypted_share)

        reconstructed_secret = self.sss.reconstruct_secret(decrypted_shares)
        return reconstructed_secret

def main():
    # Example usage
    threshold = 3
    total_parties = 5
    secret = 12345  # The secret to be shared

    smpc = SecureMultipartyComputation(threshold, total_parties)
    encrypted_shares = smpc.share_secret(secret)

    print("Encrypted Shares:")
    for i, encrypted_share in enumerate(encrypted_shares):
        print(f"Party {i + 1}: Encrypted Share {encrypted_share}")

    # Simulate parties sending shares
    selected_encrypted_shares = random.sample(encrypted_shares, threshold)
    print("\nSelected Encrypted Shares for Reconstruction:")
    for i, encrypted_share in enumerate(selected_encrypted_shares):
        print(f"Party {i + 1}: Encrypted Share {encrypted_share}")

    reconstructed_secret = smpc.reconstruct_secret(selected_encrypted_shares)
    print(f"\nReconstructed Secret: {reconstructed_secret}")

if __name__ == "__main__":
    main()
