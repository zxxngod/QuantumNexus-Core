import os

class Config:
    """Configuration class to hold application settings."""
    
    # Ethereum node provider URL
    PROVIDER_URL = os.getenv("PROVIDER_URL", "https://your.ethereum.node")
    
    # Private key for the account
    PRIVATE_KEY = os.getenv("PRIVATE_KEY", "0xYourPrivateKey")
    
    # Log file settings
    LOG_FILE = os.getenv("LOG_FILE", "app.log")
    
    # Other configuration settings can be added here
    # For example, database settings, API keys, etc.
    
    @staticmethod
    def display_config():
        """Display the current configuration settings."""
        print("Current Configuration:")
        print(f"Provider URL: {Config.PROVIDER_URL}")
        print(f"Log File: {Config.LOG_FILE}")
        # Add more settings as needed

if __name__ == "__main__":
    Config.display_config()
