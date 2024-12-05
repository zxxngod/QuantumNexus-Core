import numpy as np
from hashlib import sha3_256
from random import SystemRandom
import json

class NTRU:
    def __init__(self, p=3, q=64, N=11):
        self.p = p  # Small modulus
        self.q = q  # Large modulus
        self.N = N  # Polynomial degree
        self.random = SystemRandom()  # Cryptographically secure random number generator
        self.f, self.g = self.generate_polynomials()
        self.h = self.calculate_public_key()

    def generate_polynomials(self):
        """Generate two random polynomials with coefficients in {-1, 0, 1}."""
        f = self.generate_polynomial()
        g = self.generate_polynomial()
        return f, g

    def generate_polynomial(self):
        """Generate a random polynomial with coefficients in {-1, 0, 1}."""
        return np.random.choice([-1, 0, 1], size=self.N)

    def calculate_public_key(self):
        """Calculate the public key h = (q * g) / f mod q."""
        f_inv = self.modular_inverse(self.f, self.q)
        h = (self.poly_multiply(self.g, f_inv) % self.q) % self.q
        return h

    def modular_inverse(self, a, m):
        """Compute the modular inverse of a mod m using Extended Euclidean Algorithm."""
        m0, x0, x1 = m, 0, 1
        if m == 1:
            return 0
        while a > 1:
            q = a // m
            m, a = a % m, m
            x0, x1 = x1 - q * x0, x0
        return x1 + m0 if x1 < 0 else x1

    def encrypt(self, message):
        """Encrypt a message using the public key."""
        if len(message) != self.N:
            raise ValueError("Message length must be equal to N.")
        r = self.generate_polynomial()  # Random polynomial
        e = (self.p * r + message) % self.q  # Encrypt the message
        return e

    def decrypt(self, e):
        """Decrypt the ciphertext using the private key."""
        a = self.poly_multiply(e, self.f) % self.q
        return a

    def poly_multiply(self, a, b):
        """Multiply two polynomials a and b."""
        result = np.zeros(2 * self.N - 1, dtype=int)
        for i in range(self.N):
            for j in range(self.N):
                result[i + j] += a[i] * b[j]
        return result[:self.N]  # Return only the first N coefficients

    def hash_message(self, message):
        """Hash the message using SHA-3."""
        return sha3_256(message.encode()).hexdigest()

    def serialize_key(self):
        """Serialize the public and private keys to JSON format."""
        return json.dumps({
            'f': self.f.tolist(),
            'g': self.g.tolist(),
            'h': self.h.tolist()
        })

    def deserialize_key(self, key_json):
        """Deserialize keys from JSON format."""
        keys = json.loads(key_json)
        self.f = np.array(keys['f'])
        self.g = np.array(keys['g'])
        self.h = np.array(keys['h'])

    def sign(self, message):
        """Sign a message using the private key."""
        hashed_message = self.hash_message(message)
        signature = self.encrypt(np.array([int(bit) for bit in hashed_message]))
        return signature

    def verify(self, message, signature):
        """Verify a signature using the public key."""
        decrypted_message = self.decrypt(signature)
        hashed_message = self.hash_message(message)
        return np.array_equal(decrypted_message, np.array([ int(bit) for bit in hashed_message]))

# Example usage
if __name__ == "__main__":
    ntru = NTRU()
    message = np.random.choice([-1, 0, 1], size=ntru.N)  # Random message
    print("Original Message:", message)

    encrypted_message = ntru.encrypt(message)
    print("Encrypted Message:", encrypted_message)

    decrypted_message = ntru.decrypt(encrypted_message)
    print("Decrypted Message:", decrypted_message)

    # Signing and verifying a message
    message_str = "Hello, this is a test message."
    signature = ntru.sign(message_str)
    print("Signature:", signature)

    is_valid = ntru.verify(message_str, signature)
    print("Signature valid:", is_valid)

    # Serialize keys
    serialized_key = ntru.serialize_key()
    print("Serialized Key:", serialized_key)

    # Deserialize keys
    ntru.deserialize_key(serialized_key)
    print("Deserialized Key:", ntru.f, ntru.g, ntru.h)
