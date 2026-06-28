from datetime import datetime


def log(result):

    print("\n------ SENTINEL LOG ------")

    print("Time:", result.timestamp)
    print("Action:", result.action)
    print("Role:", result.role)
    print("Risk Level:", result.risk)

    print("Decision:", result.decision)
    print("Reason:", result.reason)

    print("--------------------------")
