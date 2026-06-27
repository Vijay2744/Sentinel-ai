from models import DecisionContext
from rules import evaluate_decision
from logger import log_decision


def analyze_decision(user_input):

    try:

        context = DecisionContext(
            user_input=user_input
        )

        decision = evaluate_decision(context)

        audit_id = log_decision(decision)

        result = decision.to_dict()

        result["audit_id"] = audit_id

        return result

    except Exception as e:

        return {
            "error": str(e)
        }
