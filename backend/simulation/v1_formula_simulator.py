"""
PMI V1 || Client-Grade Retail Promotion Simulator
Economically realistic synthetic dataset generator.
No fragile covariance math. No deterministic tricks.
"""

import numpy as np
import pandas as pd


class V1FormulaSimulator:
    def __init__(self, seed: int = 42):
        self.seed = seed
        np.random.seed(seed)

    def generate_dataset(self, n_samples: int = 4000) -> pd.DataFrame:

        # -----------------------------
        # Core business variables
        # -----------------------------

        discount = np.clip(np.random.normal(30, 12, n_samples), 5, 70)

        # Correlated velocity (manually correlated, not covariance matrix)
        velocity = np.clip(
            np.random.normal(40 + discount * 0.8, 25, n_samples),
            1,
            200
        )

        returns = np.clip(
            np.random.normal(0.12 + discount * 0.002, 0.05, n_samples),
            0.01,
            0.5
        )

        inventory = np.clip(
            np.random.normal(600, 400, n_samples),
            10,
            10000
        )

        price = np.clip(
            np.random.normal(25000, 18000, n_samples),
            500,
            100000
        )

        support = np.clip(
            np.random.normal(0.07 + returns * 0.3, 0.03, n_samples),
            0.01,
            0.3
        )

        duration = np.random.choice([1, 3, 7, 14, 21, 30], n_samples)
        competitor = np.random.randint(0, 11, n_samples)

        segment = np.random.choice(
            ["premium", "value", "bargain"],
            n_samples,
            p=[0.3, 0.5, 0.2]
        )

        # Margin realism
        margin_before = np.random.uniform(20, 60, n_samples)

        hidden_costs = np.random.lognormal(7, 0.5, n_samples)

        # -----------------------------
        # Elastic Demand (Smooth Curve)
        # -----------------------------

        elasticity_base = 1.1 * (1 - np.exp(-discount / 35))
        elasticity_random = np.random.normal(1.0, 0.15, n_samples)
        elasticity = elasticity_base * elasticity_random

        demand_multiplier = 1 + elasticity

        raw_demand = velocity * duration * demand_multiplier
        total_units_sold = np.minimum(raw_demand, inventory * 1.2)


        discounted_price = price * (1 - discount / 100)
        gross_revenue = discounted_price * total_units_sold

        # -----------------------------
        # Cost Structure
        # -----------------------------

        cost_per_unit = price * (1 - margin_before / 100)
        total_cost = cost_per_unit * total_units_sold

        base_profit = gross_revenue - total_cost

        return_costs = discounted_price * total_units_sold * returns * 1.1
        holding_costs = inventory * 0.03 * duration
        support_costs = total_units_sold * support * 300
        hidden_cost_total = hidden_costs * 0.02

        net_profit = (
            base_profit
            - return_costs
            - holding_costs
            - support_costs
            - hidden_cost_total
        )

        # -----------------------------
        # Soft Nonlinear Economics
        # -----------------------------

        habituation_penalty = (
            (discount / 100) ** 1.4
        ) * gross_revenue * 0.05 * (duration / 30)

        competition_penalty = (
            competitor / 10
        ) * gross_revenue * 0.06

        premium_bonus = np.where(
            (segment == "premium") & (discount < 20),
            gross_revenue * 0.04,
            0
        )

        # -----------------------------
        # Realistic Heteroskedastic Noise
        # -----------------------------

        noise_scale = (
            9000
            + discount * 120
            + competitor * 800
        )

        market_noise = np.random.normal(0, noise_scale)
        execution_noise = np.random.normal(0, 12000 + discount * 80, n_samples)

        actual_profit_loss = (
            net_profit
            - habituation_penalty
            - competition_penalty
            + premium_bonus
            + market_noise
            + execution_noise
        )

        df = pd.DataFrame({
            "discount_percent": discount,
            "sales_velocity": velocity,
            "return_rate": returns,
            "inventory_level": inventory,
            "price": price,
            "support_tickets": support,
            "duration_days": duration,
            "competitor_activity": competitor,
            "customer_segment": segment,
            "margin_before": margin_before,
            "actual_profit_loss": actual_profit_loss
        })

        return df


# ------------------------------------------------------
# VALIDATION BLOCK (for GitHub credibility)
# ------------------------------------------------------

if __name__ == "__main__":

    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import Ridge
    from sklearn.metrics import r2_score
    from sklearn.preprocessing import LabelEncoder
    import xgboost as xgb

    print("Generating dataset...\n")

    simulator = V1FormulaSimulator(seed=42)
    df = simulator.generate_dataset(4000)

    print(df.head())
    print("\nDataset shape:", df.shape)

    print("\nProfit Stats:")
    print(df["actual_profit_loss"].describe())
    print("\n% Positive Profit:",
          (df["actual_profit_loss"] > 0).mean() * 100)

    X = df.drop("actual_profit_loss", axis=1)
    y = df["actual_profit_loss"]

    le = LabelEncoder()
    X["customer_segment"] = le.fit_transform(X["customer_segment"])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    linear = Ridge(alpha=10)
    linear.fit(X_train, y_train)
    r2_linear = r2_score(y_test, linear.predict(X_test))

    xgb_model = xgb.XGBRegressor(
        max_depth=6,
        n_estimators=200,
        learning_rate=0.05,
        subsample=0.8,
        random_state=42,
        verbosity=0
    )
    xgb_model.fit(X_train, y_train)
    r2_xgb = r2_score(y_test, xgb_model.predict(X_test))

    print("\nModel Performance:")
    print("Linear R²:", round(r2_linear, 4))
    print("XGBoost R²:", round(r2_xgb, 4))
