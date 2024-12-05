import os
import json
import jwt
import hashlib
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class IdentityManagement:
    def __init__(self, secret_key, algorithm='HS256'):
        self.users = {}  # In-memory user database
        self.secret_key = secret_key
        self.algorithm = algorithm

    def hash_password(self, password):
        """Hash a password using PBKDF2."""
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(password.encode())
        return salt + key  # Store salt with the key

    def verify_password(self, stored_password, provided_password):
        """Verify a stored password against one provided by user."""
        salt = stored_password[:16]
        stored_key = stored_password[16:]
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        try:
            kdf.verify(provided_password.encode(), stored_key)
            return True
        except Exception:
            return False

    def register_user(self, username, password):
        """Register a new user."""
        if username in self.users:
            raise ValueError("User  already exists.")
        hashed_password = self.hash_password(password)
        self.users[username] = {
            'password': hashed_password,
            'roles': []
        }
        print(f"User  '{username}' registered successfully.")

    def authenticate_user(self, username, password):
        """Authenticate a user and return a JWT token."""
        if username not in self.users:
            raise ValueError("User  does not exist.")
        if not self.verify_password(self.users[username]['password'], password):
            raise ValueError("Invalid password.")
        
        # Create JWT token
        token = jwt.encode({
            'sub': username,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=1)  # Token valid for 1 hour
        }, self.secret_key, algorithm=self.algorithm)
        
        return token

    def add_role(self, username, role):
        """Add a role to a user."""
        if username not in self.users:
            raise ValueError("User  does not exist.")
        if role not in self.users[username]['roles']:
            self.users[username]['roles'].append(role)
            print(f"Role '{role}' added to user '{username}'.")

    def check_role(self, username, role):
        """Check if a user has a specific role."""
        if username not in self.users:
            raise ValueError("User  does not exist.")
        return role in self.users[username]['roles']

    def decode_token(self, token):
        """Decode a JWT token and return the payload."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired.")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token.")

if __name__ == "__main__":
    secret_key = os.urandom(32)  # Generate a random secret key
    identity_manager = IdentityManagement(secret_key)

    # Example usage
    identity_manager.register_user("alice", "securepassword123")
    token = identity_manager.authenticate_user("alice", "securepassword123")
    print(f"JWT Token for Alice: {token}")

    identity_manager.add_role("alice", "admin")
    print(f"Alice has admin role: {identity_manager.check_role('alice', 'admin')}")

    # Decode the token
    payload = identity_manager.decode_token(token)
    print(f"Decoded token payload: {json.dumps(payload, indent=2)}")
