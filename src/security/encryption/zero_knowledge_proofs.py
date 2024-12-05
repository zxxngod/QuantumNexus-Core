import hashlib
import random

class ZeroKnowledgeProof:
    def __init__(self, p, g, x):
        """
        Initialize the zero-knowledge proof system.
        
        :param p: A large prime number.
        :param g: A generator of the group.
        :param x: The secret (private key) known only to the prover.
        """
        self.p = p
        self.g = g
        self.x = x  # Secret key
        self.y = pow(g, x, p)  # Public key

    def generate_commitment(self):
        """
        Generate a random commitment.
        
        :return: A tuple (r, t) where r is the random nonce and t is the commitment.
        """
        r = random.randint(1, self.p - 1)  # Random nonce
        t = pow(self.g, r, self.p)  # Commitment
        return r, t

    def generate_challenge(self, t):
        """
        Generate a challenge for the verifier.
        
        :param t: The commitment.
        :return: The challenge (hash).
        """
        # Hash the commitment to create a challenge
        challenge = hashlib.sha256(str(t).encode()).hexdigest()
        return challenge

    def generate_response(self, r, challenge):
        """
        Generate a response to the challenge.
        
        :param r: The random nonce.
        :param challenge: The challenge from the verifier.
        :return: The response.
        """
        # Convert challenge to integer
        challenge_int = int(challenge, 16)
        response = (r + challenge_int * self.x) % (self.p - 1)
        return response

    def verify(self, t, challenge, response):
        """
        Verify the zero-knowledge proof.
        
        :param t: The commitment.
        :param challenge: The challenge from the verifier.
        :param response: The response from the prover.
        :return: True if the proof is valid, False otherwise.
        """
        # Convert challenge to integer
        challenge_int = int(challenge, 16)
        
        # Calculate the left-hand side of the verification equation
        left = (pow(self.g, response, self.p) * pow(self.y, challenge_int, self.p)) % self.p
        
        # The right-hand side is the commitment
        return left == t

# Example usage
if __name__ == "__main__":
    # Parameters for the zero-knowledge proof
    p = 23  # A small prime number for demonstration
    g = 5   # A generator of the group
    x = 6   # Secret key (private)

    # Initialize the zero-knowledge proof system
    zk_proof = ZeroKnowledgeProof(p, g, x)

    # Prover generates a commitment
    r, t = zk_proof.generate_commitment()
    print(f"Commitment (t): {t}")

    # Prover generates a challenge
    challenge = zk_proof.generate_challenge(t)
    print(f"Challenge: {challenge}")

    # Prover generates a response
    response = zk_proof.generate_response(r, challenge)
    print(f"Response: {response}")

    # Verifier checks the proof
    is_valid = zk_proof.verify(t, challenge, response)
    print(f"Is the proof valid? {is_valid}")
