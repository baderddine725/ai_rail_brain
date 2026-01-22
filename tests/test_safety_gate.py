# tests/test_safety_gate.py
from app.core.safety_gate import SafetyGate

def test_validate_safety_success():
    gate = SafetyGate()
    proposal = {"headway_seconds": 150, "platform_load": 0.7}
    assert gate.validate(proposal) is True

def test_validate_safety_failure_headway():
    gate = SafetyGate()
    # Danger : trains trop proches (60s au lieu de 120s)
    proposal = {"headway_seconds": 60, "platform_load": 0.7}
    assert gate.validate(proposal) is False