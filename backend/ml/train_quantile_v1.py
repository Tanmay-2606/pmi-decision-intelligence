from backend.simulation.v1_formula_simulator import V1FormulaSimulator
from backend.ml.quantile_ensemble import QuantileEnsemble
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

if __name__ == "__main__":

    print("\n=== STEP 1: Generating Dataset ===")

    simulator = V1FormulaSimulator(seed=42)
    df = simulator.generate_dataset(4000)

    print("Dataset shape:", df.shape)

    X = df.drop("actual_profit_loss", axis=1)
    y = df["actual_profit_loss"]

    # Encode categorical column
    if "customer_segment" in X.columns:
        le = LabelEncoder()
        X["customer_segment"] = le.fit_transform(X["customer_segment"])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("\n=== STEP 2: Training Quantile Ensemble ===")

    model = QuantileEnsemble(
        client_id="demo_client",
        simulator_version="v1"
    )

    model.fit(
        X_train,
        y_train,
        data_version="sim_v1_4000",
        data_source="simulator"
    )

    model.deploy()

    print("\n=== STEP 3: Saving Model ===")

    model.save("backend/storage/models/demo_client_v1.pkl")

    print("\n✅ Quantile model trained and saved successfully.")
