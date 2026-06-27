from rules import evaluate_decision
from logger import log_decision


def analyze_decision(user_input):

    decision = evaluate_decision(user_input)

    print(decision.to_dict())

    log_decision(decision)

    return decision.to_dict()
