import sys
import os
import uvicorn

if __name__ == "__main__":
    # Add the current directory to sys.path to resolve src modules
    current_dir = os.path.abspath(".")
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    print(f"Initializing AETHERIUM GENESIS System...")
    print(f"Root Directory: {current_dir}")
    print("Target: src.backend.server:app")

    # Run Uvicorn
    # Using reload=True for development convenience as requested
    uvicorn.run("src.backend.server:app", host="0.0.0.0", port=8000, reload=True)
