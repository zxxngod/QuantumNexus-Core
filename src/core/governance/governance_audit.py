import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GovernanceAudit:
    def __init__(self):
        self.audit_log = []
        logger.info("Governance audit system initialized.")

    def log_action(self, action_description):
        """Log an action taken in the governance framework."""
        self.audit_log.append(action_description)
        logger.info(f"Action logged: {action_description}")

    def display_audit_log(self):
        """Display the audit log."""
        logger.info("Audit Log:")
        for entry in self.audit_log:
            logger.info(entry)

if __name__ == "__main__":
    audit_system = GovernanceAudit()
    audit_system.log_action("Member 0xMemberAddress1 added.")
    audit_system.log_action("Proposal 'Increase budget' created.")
    audit_system.display_audit_log()
