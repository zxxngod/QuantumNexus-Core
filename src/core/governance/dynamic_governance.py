import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DynamicGovernance:
    def __init__(self, reputation_system):
        self.reputation_system = reputation_system
        logger.info("Dynamic governance system initialized.")

    def calculate_voting_power(self, member_address):
        """Calculate voting power based on reputation."""
        reputation = self.reputation_system.get_reputation(member_address)
        voting_power = max(1, reputation // 10)  # Example: 1 vote for every 10 reputation points
        logger.info(f"Voting power for {member_address}: {voting_power}")
        return voting_power

    def adjust_proposal_weight(self, proposal):
        """Adjust proposal weight based on member participation."""
        total_weight = 0
        for voter in proposal['voters']:
            weight = self.calculate_voting_power(voter)
            total_weight += weight
        logger.info(f"Total weight for proposal '{proposal['description']}': {total_weight}")
        return total_weight

if __name__ == "__main__":
    from reputation_system import ReputationSystem

    reputation_system = ReputationSystem()
    reputation_system.update_reputation("0xMemberAddress1", 20)
    reputation_system.update_reputation("0xMemberAddress2", 5)

    dynamic_governance = DynamicGovernance(reputation_system)
    voting_power = dynamic_governance.calculate_voting_power("0xMemberAddress1")
    logger.info(f"Voting power for 0xMemberAddress1: {voting_power}")
