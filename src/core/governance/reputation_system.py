import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReputationSystem:
    def __init__(self):
        self.reputation_scores = {}
        logger.info("Reputation system initialized.")

    def update_reputation(self, member_address, change):
        """Update the reputation score of a member."""
        if member_address not in self.reputation_scores:
            self.reputation_scores[member_address] = 0
        self.reputation_scores[member_address] += change
        logger.info(f"Reputation updated for {member_address}: {self.reputation_scores[member_address]}")

    def get_reputation(self, member_address):
        """Get the reputation score of a member."""
        return self.reputation_scores.get(member_address, 0)

    def display_reputations(self):
        """Display all members' reputations."""
        logger.info("Current Reputation Scores:")
        for member, score in self.reputation_scores.items():
            logger.info(f"{member}: {score}")

if __name__ == "__main__":
    reputation_system = ReputationSystem()
    reputation_system.update_reputation("0xMemberAddress1", 10)
    reputation_system.update_reputation("0xMemberAddress2", 5)
    reputation_system.display_reputations()
