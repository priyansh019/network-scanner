# modules/risk_classifier.py

def classify_risk(severity):
    """
    Convert severity level into a readable risk message.

    Args:
        severity (str): LOW, MEDIUM, HIGH, CRITICAL

    Returns:
        str
    """

    severity = severity.upper()

    risk_levels = {
        "LOW": "Minor Risk",
        "MEDIUM": "Moderate Risk",
        "HIGH": "Dangerous",
        "CRITICAL": "Immediate Action Required"
    }

    return risk_levels.get(severity, "Unknown Risk")


# Testing
if __name__ == "__main__":

    severities = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

    for level in severities:
        print(f"{level} -> {classify_risk(level)}")