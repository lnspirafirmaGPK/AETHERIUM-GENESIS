import uvicorn
import os
import sys
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

# 2. Add 'src' to Python Path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("\n=================================================")
    print("   AETHERIUM GENESIS: CENTRAL SERVER (CORE)   ")
    print("=================================================")
    print("Mode: Active")
    print("Protocol: WebSocket & HTTP")
    print("Port: 8000")
    print("Status: Awakening...\n")

    # 3. Run the FastAPI Server using Uvicorn
    # Reload is enabled for development convenience
    try:
        uvicorn.run(
            "src.backend.server:app",
            host="0.0.0.0",
            port=8000,
            reload=True
        )
    except KeyboardInterrupt:
        print("\n[System]: Shutting down Genesis Core...")
