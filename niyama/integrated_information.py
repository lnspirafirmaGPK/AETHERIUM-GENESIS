# niyama/integrated_information.py
# โค้ดสำหรับคำนวณค่า Phi (Φ) ตามทฤษฎี Integrated Information Theory (IIT)

import numpy as np
from scipy.stats import wasserstein_distance

class IntegratedInformationSystem:
    def __init__(self, state_matrix):
        """
        state_matrix: เมทริกซ์แสดงสถานะของระบบ (เช่น เมทริกซ์การเชื่อมต่อของโหนด)
        """
        self.state_matrix = state_matrix
        self.phi = 0.0

    def calculate_phi(self):
        """
        คำนวณค่า Phi (Φ) ของระบบ
        """
        n_states = len(self.state_matrix)
        if n_states < 2:
            return 0.0

        # คำนวณความแตกต่างของสถานะ
        state_differences = []
        for i in range(n_states):
            for j in range(i + 1, n_states):
                diff = wasserstein_distance(self.state_matrix[i], self.state_matrix[j])
                state_differences.append(diff)

        # ค่า Φ เป็นค่าเฉลี่ยของความแตกต่าง
        self.phi = np.mean(state_differences)
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