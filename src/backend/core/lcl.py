import time
import uuid
from typing import Dict, List, Deque, Optional
from collections import deque
from .light_schemas import (
    LightIntent, LightInstruction, LightAction, LightEntity, LightState, PriorityLevel
)
from .formation_manager import FormationManager

class LightControlLogic:
    """
    Light Control Logic (LCL)
    Translates abstract LightIntent into concrete LightInstruction for the renderer.
    Must be deterministic.
    """

    def __init__(self):
        # Gatekeeper State
        self.last_intent_time: Dict[str, float] = {}
        self.intent_timestamps: Dict[str, Deque[float]] = {} # Sliding window for rate limit
        self.RATE_LIMIT = 5.0 # intents per second per source
        self.WINDOW_SIZE = 1.0 # seconds

        # Physics State
        self.entities: Dict[str, LightEntity] = {}
        self.system_energy: float = 100.0
        self.MAX_ENERGY = 100.0

        # Metrics
        self.metrics = {
            "latency": deque(maxlen=100),
            "intent_count": 0
        }

    def _check_rate_limit(self, source: str) -> bool:
        """
        Returns True if allowed, False if rate limited.
        """
        if source not in self.intent_timestamps:
            self.intent_timestamps[source] = deque()

        now = time.time()
        timestamps = self.intent_timestamps[source]

        # Remove old timestamps
        while timestamps and timestamps[0] < now - self.WINDOW_SIZE:
            timestamps.popleft()

        if len(timestamps) >= self.RATE_LIMIT:
            return False

        timestamps.append(now)
        return True

    def _check_priority(self, intent: LightIntent) -> bool:
        """
        Returns True if intent should be processed based on priority.
        """
        if intent.priority < PriorityLevel.AMBIENT:
             return False
        return True

    def _check_harmony(self, intent: LightIntent) -> LightIntent:
        """
        Modifies intent to enforce harmony rules (e.g. velocity caps).
        """
        # Velocity cap
        if intent.vector:
            vx, vy = intent.vector
            magnitude = (vx**2 + vy**2)**0.5
            MAX_VELOCITY = 1.0
            if magnitude > MAX_VELOCITY:
                scale = MAX_VELOCITY / magnitude
                intent.vector = (vx * scale, vy * scale)

        # Brightness/Intensity cap
        if intent.intensity is not None and intent.intensity > 1.0:
            intent.intensity = 1.0

        return intent

    def _deduct_energy(self, action: LightAction) -> bool:
        cost = 0.0
        if action == LightAction.MOVE: cost = 0.5
        elif action == LightAction.SPAWN: cost = 2.0
        elif action == LightAction.ERASE: cost = 0.2
        elif action == LightAction.EMPHASIZE: cost = 0.1
        elif action == LightAction.MANIFEST: cost = 5.0 # High cost
        elif action == LightAction.ANSWER: cost = 0.5

        if self.system_energy >= cost:
            self.system_energy -= cost
            return True
        return False

    def process(self, intent: LightIntent) -> Optional[LightInstruction]:
        start_time = time.time()
        instruction = self._process_internal(intent)

        # Metrics
        latency = (time.time() - start_time) * 1000
        self.metrics["latency"].append(latency)
        self.metrics["intent_count"] += 1

        return instruction

    def _process_internal(self, intent: LightIntent) -> Optional[LightInstruction]:
        # Gatekeeper checks
        if not self._check_rate_limit(intent.source):
            return None

        if not self._check_priority(intent):
            return None

        intent = self._check_harmony(intent)

        # Metabolism
        if not self._deduct_energy(intent.action):
            # Energy depleted
            if intent.action == LightAction.SPAWN:
                return None
            return None

        # Update last activity
        self.last_intent_time[intent.source] = time.time()

        instruction = None

        # Physics Update
        if intent.action == LightAction.SPAWN:
            # Create entity
            entity_id = str(uuid.uuid4())
            # Determine position from region center
            region = intent.region or (0.4, 0.4, 0.6, 0.6)
            x = (region[0] + region[2]) / 2
            y = (region[1] + region[3]) / 2

            # Deterministic color based on intent or random
            entity = LightEntity(
                id=entity_id,
                position=(x, y),
                velocity=(0.0, 0.0),
                energy=1.0,
                history=[]
            )
            self.entities[entity_id] = entity

            instruction = LightInstruction(
                intent=LightAction.SPAWN,
                target=entity_id,
                region=intent.region,
                color_profile=intent.color_hint or "natural_green",
                shape="organic"
            )

        elif intent.action == LightAction.MOVE:
            # Apply force/velocity
            vec = intent.vector or (0.0, 0.0)
            strength = intent.intensity if intent.intensity is not None else 1.0

            # Apply to target or all
            targets = []
            if intent.target and intent.target in self.entities:
                targets = [self.entities[intent.target]]
            elif not intent.target or intent.target == "GLOBAL":
                targets = list(self.entities.values())

            for ent in targets:
                # Break target lock if moving manually
                ent.target_position = None

                vx, vy = ent.velocity
                # F=ma, assume m=1. dv = F*dt. Assume intent applies instant impulse.
                # Scale force significantly
                impulse_scale = 0.05
                ent.velocity = (vx + vec[0] * strength * impulse_scale, vy + vec[1] * strength * impulse_scale)

            instruction = LightInstruction(
                intent=LightAction.MOVE,
                target=intent.target,
                vector=vec,
                strength=strength
            )

        elif intent.action == LightAction.ERASE:
            if intent.region:
                # Erase entities in region
                to_remove = []
                r = intent.region
                for eid, ent in self.entities.items():
                    px, py = ent.position
                    if r[0] <= px <= r[2] and r[1] <= py <= r[3]:
                        to_remove.append(eid)
                for eid in to_remove:
                    del self.entities[eid]
            else:
                self.entities.clear()

            instruction = LightInstruction(intent=LightAction.ERASE, region=intent.region)

        elif intent.action == LightAction.EMPHASIZE:
             instruction = LightInstruction(
                intent=LightAction.EMPHASIZE,
                target=intent.target,
                strength=intent.intensity or 1.0,
                color_profile=intent.color_hint or "bright",
                text_content=intent.text_content
            )

        elif intent.action == LightAction.ANSWER:
             instruction = LightInstruction(
                intent=LightAction.ANSWER,
                text_content=intent.text_content
             )

        elif intent.action == LightAction.MANIFEST:
            # Generate formation data if shape name is provided but no raw data
            if not intent.formation_data and intent.shape_name:
                count = len(self.entities) if self.entities else 50
                count = max(count, 30) # Ensure minimal density
                intent.formation_data = FormationManager.get_formation(intent.shape_name, count)

            if intent.formation_data:
                # Match particles to targets
                # If we need more particles, spawn them
                current_ids = list(self.entities.keys())
                target_count = len(intent.formation_data)
                current_count = len(current_ids)

                # Spawn if needed
                if current_count < target_count:
                    needed = target_count - current_count
                    for _ in range(needed):
                        eid = str(uuid.uuid4())
                        # Spawn near center initially
                        self.entities[eid] = LightEntity(
                            id=eid,
                            position=(0.5, 0.5),
                            velocity=(0.0, 0.0),
                            energy=1.0
                        )

                # Assign targets
                entity_ids = list(self.entities.keys())
                for i, (tx, ty, color) in enumerate(intent.formation_data):
                    if i < len(entity_ids):
                        eid = entity_ids[i]
                        self.entities[eid].target_position = (tx, ty)
                        self.entities[eid].target_color = color

                # If we have excess particles, maybe release them or let them float
                # For now, just leave them

            instruction = LightInstruction(
                intent=LightAction.MANIFEST,
                text_content=intent.text_content,
                formation_data=intent.formation_data
            )

        return instruction

    def tick(self, dt: float) -> LightState:
        # Physics Step
        for entity in self.entities.values():
            x, y = entity.position
            vx, vy = entity.velocity

            # Formation Physics (Target Seeking)
            if entity.target_position:
                tx, ty = entity.target_position

                # Proportional Control (Spring force)
                k_p = 5.0  # Spring constant
                k_d = 0.5  # Damping

                dx = tx - x
                dy = ty - y

                fx = k_p * dx - k_d * vx
                fy = k_p * dy - k_d * vy

                vx += fx * dt
                vy += fy * dt

            else:
                # Regular drift/friction if no target
                vx *= 0.95
                vy *= 0.95

            x += vx * dt
            y += vy * dt

            # Bounce/Clamp
            if x < 0: x = 0; vx = -vx * 0.8
            if x > 1: x = 1; vx = -vx * 0.8
            if y < 0: y = 0; vy = -vy * 0.8
            if y > 1: y = 1; vy = -vy * 0.8

            entity.position = (x, y)
            entity.velocity = (vx, vy)

            # History
            entity.history.append((x, y))
            if len(entity.history) > 10:
                entity.history.pop(0)

        # Energy Regeneration
        # If last activity > 1.0s, regenerate
        last_activity = max(self.last_intent_time.values()) if self.last_intent_time else 0
        if time.time() - last_activity > 1.0:
            self.system_energy = min(self.MAX_ENERGY, self.system_energy + 5.0 * dt)

        return LightState(
            entities=self.entities,
            system_energy=self.system_energy
        )

    def get_metrics(self) -> Dict:
        avg_latency = sum(self.metrics["latency"]) / len(self.metrics["latency"]) if self.metrics["latency"] else 0.0
        return {
            "avg_latency_ms": avg_latency,
            "total_intents": self.metrics["intent_count"],
            "system_energy": self.system_energy,
            "entity_count": len(self.entities)
        }
