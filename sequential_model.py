"""
Pure-Python sequential model of the exact hypothesized causal chain:

Mechanical fundic ballooning
  → exaggerated vagal afferent traffic
  → brainstem-mediated, rhythmically disordered LES relaxation
    + phrenic inhibition of the crural diaphragm
  → repeated loss of the antireflux barrier
  → retrograde reflux
  → secondary neural sensitization
"""

from dataclasses import dataclass
from typing import List
import time


@dataclass
class StepResult:
    stage: str
    value: float
    description: str


class CausalChainSimulator:
    def __init__(self):
        self.fundic_ballooning = 0.0
        self.vagal_afferent = 0.0
        self.brainstem_drive = 0.0
        self.les_tone = 1.0
        self.crural_tone = 1.0
        self.barrier = 1.0
        self.reflux = 0.0
        self.sensitization = 0.0
        self.history: List[StepResult] = []

    def run_chain(self, ballooning_intensity: float = 0.85, steps: int = 8):
        """
        Execute the full hypothesized causal sequence iteratively.
        """
        print("Hypothesized causal chain simulation")
        print("=" * 70)
        print(f"{'Step':<6} {'Stage':<35} {'Value':>8}  Description")
        print("-" * 70)

        self.fundic_ballooning = max(0.0, min(1.0, ballooning_intensity))

        for t in range(steps):
            # 1. Mechanical fundic ballooning
            self._record("1. Fundic ballooning", self.fundic_ballooning,
                         "Mechanical stretch of proximal stomach")

            # 2. Exaggerated vagal afferent traffic
            #    (amplified by existing sensitization)
            self.vagal_afferent = min(1.0, self.fundic_ballooning * 1.25 * (1.0 + self.sensitization))
            self._record("2. Vagal afferent traffic", self.vagal_afferent,
                         "Stretch receptors → high-frequency vagal signals")

            # 3. Brainstem-mediated disordered output
            self.brainstem_drive = self.vagal_afferent
            self._record("3. Brainstem drive", self.brainstem_drive,
                         "NTS integrates signal → disordered motor commands")

            # 4a. Rhythmically disordered LES relaxation (vagal)
            self.les_tone = max(0.0, 1.0 - self.brainstem_drive * 1.15)
            self._record("4a. LES tone", self.les_tone,
                         "Vagal efferent → transient LES relaxation")

            # 4b. Phrenic inhibition of crural diaphragm
            self.crural_tone = max(0.0, 1.0 - self.brainstem_drive * 0.95)
            self._record("4b. Crural diaphragm tone", self.crural_tone,
                         "Phrenic inhibition → loss of diaphragmatic barrier")

            # 5. Repeated loss of the antireflux barrier
            self.barrier = (self.les_tone + self.crural_tone) / 2.0
            self._record("5. Antireflux barrier", self.barrier,
                         "Combined LES + crural pressure collapses")

            # 6. Retrograde reflux
            if self.barrier < 0.40:
                self.reflux = min(1.0, self.reflux + 0.18)
            else:
                self.reflux = max(0.0, self.reflux - 0.05)
            self._record("6. Retrograde reflux", self.reflux,
                         "Gastric contents flow into esophagus")

            # 7. Secondary neural sensitization (feeds back)
            if self.reflux > 0.3:
                self.sensitization = min(1.0, self.sensitization + 0.07)
            else:
                self.sensitization = max(0.0, self.sensitization - 0.02)
            self._record("7. Neural sensitization", self.sensitization,
                         "Vagal afferents become hyper-responsive (feedback)")

            print("-" * 70)
            time.sleep(0.15)  # slight pause for readability

        print("\nFinal state of the hypothesized loop:")
        print(f"  Fundic ballooning     : {self.fundic_ballooning:.2f}")
        print(f"  Vagal afferent traffic: {self.vagal_afferent:.2f}")
        print(f"  Brainstem drive       : {self.brainstem_drive:.2f}")
        print(f"  LES tone              : {self.les_tone:.2f}")
        print(f"  Crural tone           : {self.crural_tone:.2f}")
        print(f"  Barrier pressure      : {self.barrier:.2f}")
        print(f"  Retrograde reflux     : {self.reflux:.2f}")
        print(f"  Neural sensitization  : {self.sensitization:.2f}")

    def _record(self, stage: str, value: float, description: str):
        result = StepResult(stage, value, description)
        self.history.append(result)
        print(f"{len(self.history):<6} {stage:<35} {value:8.2f}  {description}")


# ----------------------------------------------------------------------
if __name__ == "__main__":
    sim = CausalChainSimulator()
    sim.run_chain(ballooning_intensity=0.88, steps=6)
