import logging
from web3 import Web3
from eth_account import Account

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DAO:
    def __init__(self, provider_url, private_key):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.account = Account.from_key(private_key)
        self.members = set()
        self.proposals = []
        logger.info("DAO initialized.")

    def add_member(self, member_address):
        """Add a member to the DAO."""
        if member_address not in self.members:
            self.members.add(member_address)
            logger.info(f"Member {member_address} added to the DAO.")
        else:
            logger.warning(f"Member {member_address} is already in the DAO.")

    def remove_member(self, member_address):
        """Remove a member from the DAO."""
        if member_address in self.members:
            self.members.remove(member_address)
            logger.info(f"Member {member_address} removed from the DAO.")
        else:
            logger.warning(f"Member {member_address} is not in the DAO.")

    def create_proposal(self, description):
        """Create a new proposal."""
        proposal = {
            'description': description,
            'votes_for': 0,
            'votes_against': 0,
            'voters': set(),
            'executed': False
        }
        self.proposals.append(proposal)
        logger.info(f"Proposal created: {description}")

    def vote(self, proposal_index, vote_for):
        """Vote on a proposal."""
        if proposal_index < 0 or proposal_index >= len(self.proposals):
            logger.error("Invalid proposal index.")
            return

        proposal = self.proposals[proposal_index]
        voter = self.account.address

        if voter in proposal['voters']:
            logger.warning("You have already voted on this proposal.")
            return

        if vote_for:
            proposal['votes_for'] += 1
        else:
            proposal['votes_against'] += 1

        proposal['voters'].add(voter)
        logger.info(f"Voted {'for' if vote_for else 'against'} proposal: {proposal['description']}")

    def execute_proposal(self, proposal_index):
        """Execute a proposal if it has enough votes."""
        if proposal_index < 0 or proposal_index >= len(self.proposals):
            logger.error("Invalid proposal index.")
            return

        proposal = self.proposals[proposal_index]

        if proposal['executed']:
            logger.warning("Proposal has already been executed.")
            return

        # Simple majority rule for execution
        if proposal['votes_for'] > proposal['votes_against']:
            proposal['executed'] = True
            logger.info(f"Proposal executed: {proposal['description']}")
        else:
            logger.info(f"Proposal not executed: {proposal['description']}")

if __name__ == "__main__":
    provider_url = "https://your.ethereum.node"  # Replace with your Ethereum node URL
    private_key = "0xYourPrivateKey"  # Replace with your private key

    # Initialize the DAO
    dao = DAO(provider_url, private_key)

    # Add members to the DAO
    dao.add_member("0xMemberAddress1")  # Replace with actual member address
    dao.add_member("0xMemberAddress2")  # Replace with actual member address

    # Create a proposal
    dao.create_proposal("Increase the budget for marketing.")

    # Vote on the proposal
    dao.vote(0, vote_for=True)  # Vote for the first proposal
    dao.vote(0, vote_for=False)  # Vote against the first proposal

    # Execute the proposal
    dao.execute_proposal(0)
