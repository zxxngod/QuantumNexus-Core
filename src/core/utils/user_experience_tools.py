import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def format_proposal_output(proposal):
    """Format proposal details for user-friendly display."""
    return f"Proposal ID: {proposal['id']}\nTitle: {proposal['title']}\nDescription: {proposal['description']}\nStatus: {proposal['status']}"

def display_proposals(proposals):
    """Display a list of proposals in a user-friendly format."""
    logger.info("Displaying proposals:")
    for proposal in proposals:
        formatted_output = format_proposal_output(proposal)
        print(formatted_output)
        print("-" * 40)

def user_friendly_message(message):
    """Display a user-friendly message."""
    print(f"🔔 {message}")

# Example usage
if __name__ == "__main__":
    proposals = [
        {"id": 1, "title": "Increase budget", "description": "Proposal to increase the budget for project X.", "status": "Pending"},
        {"id": 2, "title": "New feature request", "description": "Request for a new feature in the governance system.", "status": "Approved"},
    ]
    display_proposals(proposals)
    user_friendly_message("Thank you for participating in the governance process!")
