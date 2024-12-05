import os
import socket
import json
import base64
import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

class SecureCommunication:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.peer_public_key = None

    def generate_keys(self):
        """Generate a new RSA key pair."""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

    def load_keys(self, private_key_path, public_key_path):
        """Load RSA keys from files."""
        with open(private_key_path, "rb") as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )
        with open(public_key_path, "rb") as f:
            self.public_key = serialization.load_pem_public_key(
                f.read(),
                backend=default_backend()
            )

    def save_keys(self, private_key_path, public_key_path):
        """Save RSA keys to files."""
        with open(private_key_path, "wb") as f:
            f.write(self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL
            ))
        with open(public_key_path, "wb") as f:
            f.write(self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    def encrypt_message(self, message):
        """Encrypt a message using the peer's public key."""
        if self.peer_public_key is None:
            raise ValueError("Peer public key is not set.")
        
        ciphertext = self.peer_public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(ciphertext).decode()

    def decrypt_message(self, ciphertext):
        """Decrypt a message using the private key."""
        ciphertext = base64.b64decode(ciphertext.encode())
        plaintext = self.private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext.decode()

    def set_peer_public_key(self, public_key):
        """Set the peer's public key."""
        self.peer_public_key = serialization.load_pem_public_key(
            public_key.encode(),
            backend=default_backend()
        )

    def create_signature(self, message):
        """Create a digital signature for a message."""
        signature = self.private_key.sign(
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode()

    def verify_signature(self, message, signature):
        """Verify a digital signature."""
        signature = base64.b64decode(signature.encode())
        try:
            self.public_key.verify(
                signature,
                message.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False

    def start_server(self, host='localhost', port=65432):
        """Start a secure communication server."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            print(f"Server listening on {host}:{port}")
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    message = self.decrypt _message(data.decode())
                    print(f"Received message: {message}")
                    response = self.encrypt_message("Acknowledged: " + message)
                    conn.sendall(response.encode())

    def start_client(self, host='localhost', port=65432):
        """Start a secure communication client."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            message = "Hello, secure world!"
            encrypted_message = self.encrypt_message(message)
            s.sendall(encrypted_message.encode())
            data = s.recv(1024)
            print(f"Received response: {self.decrypt_message(data.decode())}")

if __name__ == "__main__":
    comm = SecureCommunication()
    comm.generate_keys()
    # Save keys for later use
    comm.save_keys("private_key.pem", "public_key.pem")

    # Example usage
    # Uncomment the following lines to run the server or client
    # comm.start_server()
    # comm.start_client()
