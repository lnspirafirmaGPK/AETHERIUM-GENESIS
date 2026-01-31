import uvicorn
import os
import sys
import socket
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

# 2. Add 'src' to Python Path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def get_local_ip():
    """Attempts to retrieve the local IP address of the machine."""
    try:
        # Create a dummy socket to connect to an external server (doesn't actually send data)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

if __name__ == "__main__":
    local_ip = get_local_ip()
    port = 8000

    print("\n=================================================")
    print("   AETHERIUM GENESIS: CENTRAL SERVER (CORE)   ")
    print("=================================================")
    print(f"Mode: Active (The Radiant Sun)")
    print(f"Local Access: http://localhost:{port}")
    print(f"Network Access: http://{local_ip}:{port}")
    print("Protocol: WebSocket & HTTP")
    print("Status: Awakening...\n")

    # 3. Run the FastAPI Server using Uvicorn
    # Reload is enabled for development convenience
    try:
        uvicorn.run(
            "src.backend.main:app",
            host="0.0.0.0",
            port=port,
            reload=True
        )
    except KeyboardInterrupt:
        print("\n[System]: Shutting down Genesis Core...")
