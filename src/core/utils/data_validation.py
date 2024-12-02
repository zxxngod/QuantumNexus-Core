import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_ethereum_address(address):
    """Validate Ethereum address format."""
    if re.match(r'^0x[a-fA-F0-9]{40}$', address):
        logger.info(f"Valid Ethereum address: {address}")
        return True
    logger.error(f"Invalid Ethereum address: {address}")
    return False

def validate_proposal_title(title):
    """Validate proposal title length and content."""
    if 5 <= len(title) <= 100:
        logger.info(f"Valid proposal title: {title}")
        return True
    logger.error(f"Invalid proposal title: {title}. Must be between 5 and 100 characters.")
    return False

def validate_vote_choice(choice, valid_choices):
    """Validate the voting choice against valid options."""
    if choice in valid_choices:
        logger.info(f"Valid vote choice: {choice}")
        return True
    logger.error(f"Invalid vote choice: {choice}. Valid choices are: {valid_choices}")
    return False

# Example usage
if __name__ == "__main__":
    validate_ethereum_address("0x1234567890abcdef1234567890abcdef12345678")
    validate_proposal_title("Increase budget for project X")
    validate_vote_choice("approve", ["approve", "reject", "abstain"])
