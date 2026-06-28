from dataclasses import dataclass
from datetime import datetime

@dataclass
class Decision:
    action: str
    role: str
    decision: str
    reason: str
    risk: str
    timestamp: datetime
