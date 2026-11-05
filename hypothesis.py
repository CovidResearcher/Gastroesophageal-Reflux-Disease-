"""
Pure-Python model of the hypothesized mechanism:

Ballooning distension → vagus-phrenic rhythmic feedback-loop disorder
→ transient LES relaxation + crural diaphragm inhibition
→ retrograde reflux ("retroactively refluxing indigestion")

"""

from dataclasses import dataclass, field
from typing import List
import random


@dataclass
class PhysiologicalState:
    """Current state of the system."""
    fundic_distension: float = 0.0          # 0.0 – 1.0 (ballooning intensity)
    vagal_afferent_rate: float = 0.0        # stretch-receptor firing
    brainstem_drive: float = 0.0            # integrated signal in NTS
    les_tone: float = 1.0                   # 1.0 = fully closed, 0.0 = fully relaxed
    crural_diaphragm_tone: float = 1.0      # phrenic-controlled barrier
    barrier_pressure: float = 1.0           # combined antireflux barrier
    reflux_event: bool = False
    esophageal_acid_exposure: float = 0.0
    hypersensitivity: float = 0.0           # secondary sensitization
    temperature_stimulus: float = 0.0       # >0 = heat (hot broth), <0 = cold


class VagusPhrenicLoopSimulator:
    """
    Encodes the core hypothesis as an iterative feedback loop.
    """

    def __init__(self):
        self.state = PhysiologicalState()
        self.history: List[PhysiologicalState] = []
        self.time_step = 0

    def apply_ballooning_distension(self, intensity: float):
        """Trigger: mechanical fundic stretch."""
        self.state.fundic_distension = max(0.0, min(1.0, intensity))

    def apply_temperature_control(self, heat: float):
        """
        Intervention: extreme temperature (hot broth = positive heat).
        Proposed to interrupt the dysrhythmia.
        """
        self.state.temperature_stimulus = heat

    def _update_afferents(self):
        """Mechanoreceptors → vagal afferent signaling."""
        base = self.state.fundic_distension * 1.2
        # Hypersensitivity amplifies the signal (secondary loop)
        amplified = base * (1.0 + self.state.hypersensitivity)
        self.state.vagal_afferent_rate = min(1.0, amplified)

    def _brainstem_integration(self):
        """Nucleus tractus solitarius processes stretch signals."""
        self.state.brainstem_drive = self.state.vagal_afferent_rate

        # Temperature stimulus is hypothesized to disrupt the drive
        if abs(self.state.temperature_stimulus) > 0.5:
            # Strong thermal input reduces the pathological drive
            self.state.brainstem_drive *= (1.0 - abs(self.state.temperature_stimulus) * 0.7)
            self.state.brainstem_drive = max(0.0, self.state.brainstem_drive)

    def _efferent_output(self):
        """
        Brainstem → vagal LES relaxation + phrenic inhibition of crural diaphragm.
        This is the core of the proposed rhythmic feedback-loop disorder.
        """
        drive = self.state.brainstem_drive

        # LES tone falls (TLESRs)
        self.state.les_tone = max(0.0, 1.0 - drive * 1.1)

        # Crural diaphragm inhibited via phrenic nerve
        self.state.crural_diaphragm_tone = max(0.0, 1.0 - drive * 0.9)

        # Combined barrier pressure
        self.state.barrier_pressure = (self.state.les_tone + self.state.crural_diaphragm_tone) / 2.0

    def _reflux_and_sensitization(self):
        """Loss of barrier → retrograde flow + secondary neural sensitization."""
        if self.state.barrier_pressure < 0.35 and self.state.fundic_distension > 0.4:
            self.state.reflux_event = True
            self.state.esophageal_acid_exposure += 0.15
            # Chronic exposure increases hypersensitivity (feeds back into afferents)
            self.state.hypersensitivity = min(1.0, self.state.hypersensitivity + 0.05)
        else:
            self.state.reflux_event = False
            # Slow recovery if barrier is restored
            self.state.esophageal_acid_exposure = max(0.0, self.state.esophageal_acid_exposure - 0.03)
            self.state.hypersensitivity = max(0.0, self.state.hypersensitivity - 0.01)

    def step(self):
        """One discrete time step of the hypothesized loop."""
        self._update_afferents()
        self._brainstem_integration()
        self._efferent_output()
        self._reflux_and_sensitization()

        # Record snapshot
        snapshot = PhysiologicalState(
            fundic_distension=self.state.fundic_distension,
            vagal_afferent_rate=self.state.vagal_afferent_rate,
            brainstem_drive=self.state.brainstem_drive,
            les_tone=self.state.les_tone,
            crural_diaphragm_tone=self.state.crural_diaphragm_tone,
            barrier_pressure=self.state.barrier_pressure,
            reflux_event=self.state.reflux_event,
            esophageal_acid_exposure=self.state.esophageal_acid_exposure,
            hypersensitivity=self.state.hypersensitivity,
            temperature_stimulus=self.state.temperature_stimulus,
        )
        self.history.append(snapshot)
        self.time_step += 1

    def run(self, steps: int = 20, distension: float = 0.8, heat: float = 0.0):
        """Run a short simulation."""
        self.apply_ballooning_distension(distension)
        self.apply_temperature_control(heat)

        print(f"{'t':>3} | Dist | Vagal | Brain | LES  | Crural | Barrier | Reflux | Acid  | Hyper | Temp")
        print("-" * 85)

        for t in range(steps):
            self.step()
            s = self.state
            print(f"{t:3d} | {s.fundic_distension:4.2f} | {s.vagal_afferent_rate:5.2f} | "
                  f"{s.brainstem_drive:5.2f} | {s.les_tone:4.2f} | {s.crural_diaphragm_tone:6.2f} | "
                  f"{s.barrier_pressure:7.2f} | {'YES' if s.reflux_event else ' no':6} | "
                  f"{s.esophageal_acid_exposure:5.2f} | {s.hypersensitivity:5.2f} | {s.temperature_stimulus:4.1f}")


# ----------------------------------------------------------------------
# Example usage of the hypothesis model
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Simulation 1: Ballooning distension only (pathological loop) ===")
    sim1 = VagusPhrenicLoopSimulator()
    sim1.run(steps=12, distension=0.85, heat=0.0)

    print("\n=== Simulation 2: Same distension + extreme heat (hot-broth hypothesis) ===")
    sim2 = VagusPhrenicLoopSimulator()
    sim2.run(steps=12, distension=0.85, heat=0.9)
