import uuid
import json
from datetime import datetime


def log_decision(decision):

    audit_id = str(uuid.uuid4())[:8]

    log = {
        "audit_id": audit_id,
        "timestamp": datetime.now().isoformat(),
        "risk_score": decision.risk_score,
        "risk_level": decision.risk_level,
        "decision": decision.decision,
        "workflow": decision.workflow,
        "policy": decision.policy_triggered,
        "audit_required": decision.audit_required
    }

    with open("audit_log.json", "a") as f:
        f.write(json.dumps(log) + "\n")

    return audit_id
