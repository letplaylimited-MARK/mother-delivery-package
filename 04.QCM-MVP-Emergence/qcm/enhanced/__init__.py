"""qcm.enhanced — L2-L3 enhanced modules (EPR, DW, Mahalanobis, RCS, Deadlock)"""
from epr_entanglement import EPREntanglement, EntanglementState
from dynamic_weight import DynamicWeightCalculator, Weights
from mahalanobis_distance import MahalanobisDistance, ContrastiveLoss
from rcs_hybrid import RCSHybrid, RCSResult, PersonaIndicator
from deadlock_detector import DeadlockDetector, SoftDeadlockDetector, DeadlockFactors

__all__ = [
    "EPREntanglement", "EntanglementState",
    "DynamicWeightCalculator", "Weights",
    "MahalanobisDistance", "ContrastiveLoss",
    "RCSHybrid", "RCSResult", "PersonaIndicator",
    "DeadlockDetector", "SoftDeadlockDetector", "DeadlockFactors",
]
