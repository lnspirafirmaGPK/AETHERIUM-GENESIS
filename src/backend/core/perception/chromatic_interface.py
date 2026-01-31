import sys
import os
import subprocess
import json
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger("ChromaticSanctum")

class ChromaticSanctum:
    """
    Interface to the Chromatic Core (Physics Engine).
    Can launch either the compiled binary (if available) or the Python fallback.
    """
    def __init__(self, binary_path: str = "./chromatic_core"):
        self.binary_path = binary_path
        self.process: Optional[subprocess.Popen] = None
        self.mode = "PYTHON"

        # Check if binary exists
        if os.path.exists(binary_path) and os.access(binary_path, os.X_OK):
            self.mode = "BINARY"
        else:
            self.mode = "PYTHON"
            # Resolve path to python script
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.script_path = os.path.join(base_dir, "chromatic_core.py")

    def start(self):
        """Launches the physics engine process."""
        if self.process and self.process.poll() is None:
            return

        try:
            if self.mode == "BINARY":
                logger.info(f"Launching Chromatic Core (BINARY): {self.binary_path}")
                self.process = subprocess.Popen(
                    [self.binary_path],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=sys.stderr, # Forward stderr to console
                    text=True,
                    bufsize=1 # Line buffered
                )
            else:
                logger.info(f"Launching Chromatic Core (PYTHON): {self.script_path}")
                self.process = subprocess.Popen(
                    [sys.executable, self.script_path],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=sys.stderr,
                    text=True,
                    bufsize=1
                )
        except Exception as e:
            logger.error(f"Failed to start Chromatic Core: {e}")

    def stop(self):
        """Stops the process."""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.process = None

    def send_command(self, cmd: Dict[str, Any]):
        """Sends a JSON command to the engine."""
        if not self.process or self.process.poll() is not None:
            # Attempt restart
            self.start()
            if not self.process: return

        try:
            line = json.dumps(cmd) + "\n"
            if self.process.stdin:
                self.process.stdin.write(line)
                self.process.stdin.flush()
        except (BrokenPipeError, OSError):
            logger.error("Chromatic Core pipe broken.")
            self.stop()

    def read_line(self) -> Optional[str]:
        """Reads a line from stdout (blocking). Use with care."""
        if self.process and self.process.stdout:
            return self.process.stdout.readline()
        return None
