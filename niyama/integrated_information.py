# niyama/integrated_information.py
# โค้ดสำหรับคำนวณค่า Phi (Φ) ตามทฤษฎี Integrated Information Theory (IIT)

import numpy as np
# from scipy.stats import wasserstein_distance # Optimized: replaced with vectorized NumPy implementation

class IntegratedInformationSystem:
    def __init__(self, state_matrix):
        """
        Initialize the IntegratedInformationSystem with a state matrix.
        
        Parameters:
            state_matrix (array-like): Matrix representing the system's states (for example, node connection weights or per-node state vectors). Expected shape is (n_states, ...) where each row corresponds to a state used for Phi calculation.
        """
        self.state_matrix = state_matrix
        self.phi = 0.0

    def calculate_phi(self):
        """
        Compute the system's Phi (Φ) as the mean pairwise Wasserstein distance between state vectors.
        
        Updates self.phi with the computed value.
        
        Returns:
            float: The computed Phi value (mean of all pairwise Wasserstein distances). Returns 0.0 if the system has fewer than two states.
        """
        n_states = len(self.state_matrix)
        if n_states < 2:
            return 0.0

        # Optimization: Efficient O(N log N) calculation of mean pairwise Wasserstein distances.
        # We avoid the O(N^2) memory footprint of constructing the full distance matrix.

        # Ensure input is a numpy array
        matrix = np.asarray(self.state_matrix)
        n_states, n_features = matrix.shape

        # 1. Sort state matrix along the feature axis (axis 1) to prep for Wasserstein-1 (L1 between sorted PDFs)
        # This makes each row a valid Quantile Function for the distribution
        sorted_matrix = np.sort(matrix, axis=1)

        # 2. We need to calculate the sum of L1 distances between all pairs of rows in sorted_matrix.
        # This is equivalent to summing the pairwise differences for each column independently.
        # For a single column vector v of length N, sum_{i<j} |v_i - v_j| can be computed efficiently:
        # Sort v to get u. Then sum = sum_{k=0}^{N-1} (2k - N + 1) * u_k.

        # Sort columns independently (O(D * N log N))
        sorted_cols = np.sort(sorted_matrix, axis=0)

        # Generate coefficients (2k - N + 1)
        coeffs = 2 * np.arange(n_states) - n_states + 1

        # Compute sum of pairwise differences for all columns at once using vectorization
        # (N, 1) * (N, D) -> (N, D) -> sum over axis 0 -> (D,)
        col_sums = np.sum(coeffs[:, np.newaxis] * sorted_cols, axis=0)

        # 3. Sum over all feature columns to get total sum of distances
        total_distance_sum = np.sum(col_sums)

        # 4. Calculate mean
        # Denominator = (Number of Pairs) * (Number of Features)
        num_pairs = n_states * (n_states - 1) / 2
        self.phi = total_distance_sum / (num_pairs * n_features)

        return self.phi

# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    # สร้างเมทริกซ์สถานะตัวอย่าง (3 โหนด โหนดละ 4 สถานะ)
    example_states = [
        [0.1, 0.2, 0.3, 0.4],  # สถานะของโหนดที่ 1
        [0.2, 0.3, 0.4, 0.1],  # สถานะของโหนดที่ 2
        [0.3, 0.4, 0.1, 0.2]   # สถานะของโหนดที่ 3
    ]

    system = IntegratedInformationSystem(example_states)
    phi_value = system.calculate_phi()
    print(f"ค่า Phi (Φ) ของระบบ: {phi_value:.4f}")