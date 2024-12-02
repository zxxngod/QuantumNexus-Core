import time
import logging

class PerformanceMetrics:
    def __init__(self):
        self.metrics = {
            'proposal_creation_times': [],
            'voting_times': [],
            'execution_times': []
        }
        self.logger = logging.getLogger(__name__)

    def log_proposal_creation_time(self, start_time):
        """Log the time taken to create a proposal."""
        duration = time.time() - start_time
        self.metrics['proposal_creation_times'].append(duration)
        self.logger.info(f"Proposal creation time: {duration:.2f} seconds")

    def log_voting_time(self, start_time):
        """Log the time taken to vote on a proposal."""
        duration = time.time() - start_time
        self.metrics['voting_times'].append(duration)
        self.logger.info(f"Voting time: {duration:.2f} seconds")

    def log_execution_time(self, start_time):
        """Log the time taken to execute a proposal."""
        duration = time.time() - start_time
        self.metrics['execution_times'].append(duration)
        self.logger.info(f"Execution time: {duration:.2f} seconds")

    def display_metrics(self):
        """Display the collected performance metrics."""
        self.logger.info("Performance Metrics:")
        for metric, times in self.metrics.items():
            avg_time = sum(times) / len(times) if times else 0
            self.logger.info(f"{metric}: Average time = {avg_time:.2f} seconds, Count = {len(times)}")

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    metrics = PerformanceMetrics()

    # Simulate logging times
    start_time = time.time()
    time.sleep(1)  # Simulate proposal creation time
    metrics.log_proposal_creation_time(start_time)

    start_time = time.time()
    time.sleep(0.5)  # Simulate voting time
    metrics.log_voting_time(start_time)

    start_time = time.time()
    time.sleep(0.75)  # Simulate execution time
    metrics.log_execution_time(start_time)

    metrics.display_metrics()
