from typing import Dict, Any


class SafetyGate:
    def validate(self, resolution: Dict[str, Any]) -> bool:
        """Enforces absolute regulatory and safety constraints [cite: 3, 55]"""
        # Rule 1: Headway (Minimum separation between trains)
        if resolution.get("headway_seconds", 0) < 120:
            return False 
        
        # Rule 2: Platform capacity limits [cite: 32, 54]
        if resolution.get("platform_load") > 1.0:
            return False
            
        return True