import numpy as np
from Crypto.Util import number
from hashlib import sha256

class Paillier:
    def __init__(self, bit_length=512):
        self.bit_length = bit_length
        self.n, self.g, self.lambda_, self.mu = self.generate_keypair()

    def generate_keypair(self):
        """Generate a public/private key pair."""
        p = number.getPrime(self.bit_length)
        q = number.getPrime(self.bit_length)
        n = p * q
        g = n + 1  # Common choice for g
        lambda_ = (p - 1) * (q - 1) // np.gcd(p - 1, q - 1)
        mu = self.mod_inverse(lambda_, n)
        return n, g, lambda_, mu

    def mod_inverse(self, a, m):
        """Compute the modular inverse of a mod m using Extended Euclidean Algorithm."""
        m0, x0, x1 = m, 0, 1
        if m == 1:
            return 0
        while a > 1:
            q = a // m
            m, a = a % m, m
            x0, x1 = x1 - q * x0, x0
        return x1 + m0 if x1 < 0 else x1

    def encrypt(self, plaintext):
        """Encrypt a plaintext integer."""
        if plaintext < 0:
            raise ValueError("Plaintext must be non-negative.")
        r = number.getRandomRange(1, self.n)  # Random r in [1, n)
        c = (pow(self.g, plaintext, self.n**2) * pow(r, self.n, self.n**2)) % (self.n**2)
        return c

    def decrypt(self, ciphertext):
        """Decrypt a ciphertext."""
        u = (pow(ciphertext, self.lambda_, self.n**2) - 1) // self.n
        plaintext = (u * self.mu) % self.n
        return plaintext

    def add(self, c1, c2):
        """Homomorphically add two ciphertexts."""
        return (c1 * c2) % (self.n**2)

    def encrypt_batch(self, plaintexts):
        """Encrypt a batch of plaintext integers."""
        return [self.encrypt(p) for p in plaintexts]

    def decrypt_batch(self, ciphertexts):
        """Decrypt a batch of ciphertexts."""
        return [self.decrypt(c) for c in ciphertexts]

# Example usage
if __name__ == "__main__":
    paillier = Paillier()

    # Encrypting individual values
    plaintext1 = 5
    plaintext2 = 10
    ciphertext1 = paillier.encrypt(plaintext1)
    ciphertext2 = paillier.encrypt(plaintext2)

    print("Ciphertext 1:", ciphertext1)
    print("Ciphertext 2:", ciphertext2)

    # Homomorphic addition
    ciphertext_sum = paillier.add(ciphertext1, ciphertext2)
    print("Ciphertext Sum:", ciphertext_sum)

    # Decrypting the sum
    decrypted_sum = paillier.decrypt(ciphertext_sum)
    print("Decrypted Sum:", decrypted_sum)

    # Batch encryption and decryption
    plaintexts = [1, 2, 3, 4, 5]
    ciphertexts = paillier.encrypt_batch(plaintexts)
    print("Ciphertexts Batch:", ciphertexts)

    decrypted_batch = paillier.decrypt_batch(ciphertexts)
    print("Decrypted Batch:", decrypted_batch)
