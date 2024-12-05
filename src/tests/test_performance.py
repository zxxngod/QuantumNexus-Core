import unittest
import time
from src.core.algorithms import quantum_scaling

class TestPerformance(unittest.TestCase):

    def test_scaling_performance(self):
        start_time = time.time()
        quantum_scaling.scale("large_data_set")
        duration = time.time() - start_time
        self.assertLess(duration, 2)  # Should complete in less than 2 seconds

if __name__ == '__main__':
    unittest.main()
