from security_gate import AccessController
import config
import time

def main():
    # สามารถเปลี่ยนเป็น "MOBILE" ได้ที่นี่ หรือแก้ใน config.py
    system = AccessController(device_type=config.DEFAULT_DEVICE)
    
    # เริ่มต้นระบบในสถานะหลับ
    system.ui.show_nirodha_state()
    
    print("\n--- SIMULATION STARTED ---")
    print("Press [ENTER] to simulate a 'Knock'.")
    print("Type 'exit' to quit.")

    while True:
        user_input = input()
        
        if user_input.lower() == 'exit':
            break
            
        # จำลองการรับสัญญาณเคาะเมื่อกด Enter
        system.process_knock()

        # ถ้าตื่นแล้ว ให้จบการจำลอง (หรือจะให้ทำอย่างอื่นต่อก็ได้)
        if system.state == "AWAKENED":
            print("\n[System]: Simulation Goal Reached. Shelvas is active.")
            break

if __name__ == "__main__":
    main()