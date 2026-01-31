import sys
import json
import time
import numpy as np
import logging
import select

# Set up logging to stderr so stdout is clean for JSON communication
logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger("ChromaticCore")

class PhysicsEngine:
    def __init__(self, capacity=1000):
        self.capacity = capacity
        self.count = 0
        self.pos = np.zeros((capacity, 2), dtype=np.float32)
        self.vel = np.zeros((capacity, 2), dtype=np.float32)
        self.colors = np.zeros((capacity, 3), dtype=np.uint8)
        self.energy = 100.0

    def spawn(self, count, x=0.5, y=0.5, color=(255, 255, 255)):
        available = self.capacity - self.count
        if available <= 0: return

        spawn_count = min(count, available)
        idx = self.count
        end_idx = idx + spawn_count

        # Random velocity
        self.pos[idx:end_idx] = [x, y]
        angles = np.random.rand(spawn_count) * 2 * np.pi
        speeds = np.random.rand(spawn_count) * 0.02
        self.vel[idx:end_idx, 0] = np.cos(angles) * speeds
        self.vel[idx:end_idx, 1] = np.sin(angles) * speeds
        self.colors[idx:end_idx] = color

        self.count += spawn_count

    def update(self, dt):
        if self.count == 0: return

        # Physics
        self.pos[:self.count] += self.vel[:self.count]

        # Friction
        self.vel[:self.count] *= 0.98

        # Bounds (Wrap)
        self.pos[:self.count] %= 1.0

        # Gravity (light center pull)
        center = np.array([0.5, 0.5])
        diff = center - self.pos[:self.count]
        dist = np.linalg.norm(diff, axis=1, keepdims=True)
        # Avoid div/0
        dist = np.maximum(dist, 0.01)
        force = diff / dist * 0.0001
        self.vel[:self.count] += force

    def get_state(self):
        # Return simplified state for visualization
        return {
            "type": "state_update",
            "count": int(self.count),
            "energy": float(self.energy),
            # Send first 5 particles as sample to avoid massive JSON
            "sample_pos": self.pos[:min(self.count, 5)].tolist()
        }

def main():
    logger.info("Chromatic Core (Python Fallback) Started")
    engine = PhysicsEngine()

    last_time = time.time()
    last_print = time.time()

    try:
        while True:
            # Check for input (Non-blocking)
            # select.select([sys.stdin], [], [], 0) checks if stdin has data
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                line = sys.stdin.readline()
                if not line: break # EOF
                try:
                    cmd = json.loads(line)
                    action = cmd.get("action")
                    if action == "spawn":
                        engine.spawn(cmd.get("count", 10))
                    elif action == "energy":
                        engine.energy = cmd.get("value", 100.0)
                except json.JSONDecodeError:
                    logger.error("Invalid JSON input")

            # Update Physics
            now = time.time()
            dt = now - last_time
            last_time = now

            engine.update(dt)

            # Output State (throttled to 10Hz)
            if now - last_print > 0.1:
                print(json.dumps(engine.get_state()), flush=True)
                last_print = now

            # Sleep to prevent 100% CPU
            time.sleep(0.016) # ~60 FPS

    except KeyboardInterrupt:
        logger.info("Stopping...")
    except Exception as e:
        logger.error(f"Critical Error: {e}")

if __name__ == "__main__":
    main()
