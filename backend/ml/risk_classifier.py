class RiskClassifier:
    """
    Interprets quantile predictions and assigns risk categories.

    Inputs:
        q10  -> pessimistic estimate
        q50  -> median estimate
        q90  -> optimistic estimate

    Output:
        Dictionary containing:
            - risk_level
            - spread
            - potential_loss
    """

    def __init__(self):
        pass

    def classify(self, q10: float, q50: float, q90: float):
        """
        Classify risk based on quantile predictions.
        Logic will be implemented after calibration validation.
        """
        return {
            "risk_level": None,
            "spread": None,
            "potential_loss": None
        }
