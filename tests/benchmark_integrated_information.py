
import time
import numpy as np
from niyama.integrated_information import IntegratedInformationSystem

def benchmark():
    n_states = 500
    n_features = 128
    print(f"Generating random state matrix ({n_states}x{n_features})...")
    np.random.seed(42)
    state_matrix = np.random.random((n_states, n_features))

    system = IntegratedInformationSystem(state_matrix)

    print("Starting benchmark (IntegratedInformationSystem)...")
    start_time = time.time()
    phi = system.calculate_phi()
    end_time = time.time()

    duration = end_time - start_time
    print(f"Phi: {phi}")
    print(f"Time taken: {duration:.4f} seconds")

if __name__ == "__main__":
    benchmark()
