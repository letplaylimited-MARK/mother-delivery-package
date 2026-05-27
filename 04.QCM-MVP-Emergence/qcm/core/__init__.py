"""qcm.core — L1 core modules (roles, delta, clock, calculator, detector)"""
from simple_role import (
    SimpleRole, BaseRole, RoleFactory, RoleConfig,
    create_demo_roles, create_8_roles, ROLE_CONFIG,
)
from delta import DeltaSyncer, DeltaPayload
from vector_clock import VectorClock
from calculator import ResonanceCalculator
from detector import EmergenceDetector

__all__ = [
    "SimpleRole", "BaseRole", "RoleFactory", "RoleConfig",
    "create_demo_roles", "create_8_roles", "ROLE_CONFIG",
    "DeltaSyncer", "DeltaPayload",
    "VectorClock",
    "ResonanceCalculator",
    "EmergenceDetector",
]
