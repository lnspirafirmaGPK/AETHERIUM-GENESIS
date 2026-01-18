# lnspirafirmagpk/aetherium-genesis/AETHERIUM-GENESIS-main/main.py

from security_gate import AccessController
import config
import time
from visual_engine import GunUI

def main():
    # 1. เริ่มต้นระบบ Visual Engine
    ui = GunUI()
    
    # 2. เปิดหน้าจอ Web Interface ขึ้นมาก่อน (Living UI)
    ui.launch_interface()
    
    # รอสักนิดให้ Browser เปิดขึ้นมา
    time.sleep(2)
    
    # 3. เริ่มระบบ Security (The Ritual)
    system = AccessController(device_type=config.DEFAULT_DEVICE)
    
    # แสดงสถานะหลับ (CLI) และตั้งค่า UI เริ่มต้นเป็น Chaos
    system.ui.show_nirodha_state() 
    
    print("\n--- SIMULATION STARTED ---")
    print("Press [ENTER] 3 times quickly to simulate the 'Awakening Ritual'.")
    print("Type 'exit' to quit.")

    while True:
        user_input = input()
        
        if user_input.lower() == 'exit':
            break
            
        # จำลองการรับสัญญาณเคาะ
        system.process_knock()

        # ตรวจสอบสถานะว่าตื่นหรือยัง
        if system.state == "AWAKENED":
            # เมื่อตื่นแล้ว ให้สั่ง Web Interface เปลี่ยนรูปร่างเป็นวงกลม (Standby)
            ui.morph_ui("CIRCLE")
            
            print("\n[System]: Shelvas is active. Testing Voice Mode...")
            time.sleep(1)
            
            # ทดสอบเปลี่ยนโหมดเป็น Wave (รับเสียง)
            ui.morph_ui("WAVE")
            ui.visualize_voice(3)
            time.sleep(0.5)
            ui.visualize_voice(5)
            print("\n[System]: Simulation Complete.")
            break

if __name__ == "__main__":
    main()