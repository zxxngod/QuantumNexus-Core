import logging

def validate_address(address):
    """Validate Ethereum address format."""
    if len(address) == 42 and address.startswith("0x"):
        return True
    return False

def log_error(logger, message):
    """Log an error message."""
    logger.error(message)

def log_info(logger, message):
    """Log an info message."""
    logger.info(message)

# Example usage
if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    address = "0x1234567890abcdef1234567890abcdef12345678"
    
    if validate_address(address):
        log_info(logger, f"{address} is a valid Ethereum address.")
    else:
        log_error(logger, f"{address} is not a valid Ethereum address.")
