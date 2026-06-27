from rules import evaluate_decision
from logger import log_decision


def analyze_decision(user_input):

    try:

        decision = evaluate_decision(user_input)

        log_decision(decision)

        return decision.to_dict()

    except Exception as e:

        return {
            "error": str(e)
        }
