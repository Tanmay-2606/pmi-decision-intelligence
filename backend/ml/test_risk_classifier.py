from backend.ml.risk_classifier import RiskClassifier 
def main():
    classifier = RiskClassifier()
    q10 = -5000
    q50 = 8000
    q90 = 20000
    result = classifier.classify(q10, q50, q90)
    print("Risk Classification Output:")
    print(result)
if __name__ == "__main__":
    main()

