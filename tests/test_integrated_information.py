
import unittest
import numpy as np
from scipy.stats import wasserstein_distance
from niyama.integrated_information import IntegratedInformationSystem

class TestIntegratedInformation(unittest.TestCase):
    def test_class_implementation_correctness(self):
        # Create a smaller random matrix for testing
        n_states = 50
        n_features = 20
        np.random.seed(123)
        state_matrix = np.random.random((n_states, n_features))

        # 1. Calculate Expected Result using Original Loop Logic (Reference)
        original_diffs = []
        for i in range(n_states):
            for j in range(i + 1, n_states):
                diff = wasserstein_distance(state_matrix[i], state_matrix[j])
                original_diffs.append(diff)
        expected_phi = np.mean(original_diffs)

        # 2. Calculate Actual Result using the Optimized Class
        system = IntegratedInformationSystem(state_matrix)
        actual_phi = system.calculate_phi()

        print(f"Expected Phi (Loop): {expected_phi}")
        print(f"Actual Phi (Optimized Class): {actual_phi}")

        # Verify they are close
        self.assertAlmostEqual(expected_phi, actual_phi, places=7)

if __name__ == '__main__':
    unittest.main()
