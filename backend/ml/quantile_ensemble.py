import numpy as np
import pandas as pd
import joblib

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
from pathlib import Path

from sklearn.ensemble import GradientBoostingRegressor


# ============================================================
# MODEL LIFECYCLE
# ============================================================

class ModelStatus(Enum):
    TRAINING = "training"
    TRAINED = "trained"
    DEPLOYED = "deployed"
    RETIRED = "retired"


# ============================================================
# QUANTILE ENSEMBLE (SaaS Ready)
# ============================================================

class QuantileEnsemble:
    """
    SaaS-ready quantile regression ensemble.

    Supports:
    - Multi-client isolation
    - Dataset version tracking
    - Model lifecycle management
    - Uncertainty quantification
    """

    def __init__(
        self,
        client_id: Optional[str] = None,
        simulator_version: str = "v1",
        quantiles: List[float] = [0.10, 0.50, 0.90],
        n_estimators: int = 200,
        max_depth: int = 5,
        learning_rate: float = 0.05,
        subsample: float = 0.8,
        random_state: int = 42
    ):
        self.client_id = client_id
        self.simulator_version = simulator_version

        self.quantiles = sorted(quantiles)
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.learning_rate = learning_rate
        self.subsample = subsample
        self.random_state = random_state

        self.models: Dict[float, GradientBoostingRegressor] = {}
        self.feature_names_: Optional[List[str]] = None

        self.status = ModelStatus.TRAINING
        self.deployed_at: Optional[datetime] = None
        self.retired_at: Optional[datetime] = None

        self.data_version: Optional[str] = None
        self.data_source: Optional[str] = None
        self.training_metadata_: Dict[str, Any] = {}

        self.fitted_ = False

    # --------------------------------------------------------

    def fit(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        data_version: Optional[str] = None,
        data_source: str = "unknown",
        verbose: bool = True
    ) -> "QuantileEnsemble":

        self.feature_names_ = list(X.columns)
        self.data_version = data_version
        self.data_source = data_source

        if verbose:
            print(f"\nTraining quantile ensemble for client: {self.client_id}")
            print(f"Quantiles: {self.quantiles}")
            print(f"Samples: {len(X)}")

        for alpha in self.quantiles:
            model = GradientBoostingRegressor(
                loss="quantile",
                alpha=alpha,
                n_estimators=self.n_estimators,
                max_depth=self.max_depth,
                learning_rate=self.learning_rate,
                subsample=self.subsample,
                random_state=self.random_state
            )

            model.fit(X, y)
            self.models[alpha] = model

            if verbose:
                print(f"  ✓ Trained quantile {alpha}")

        self.training_metadata_ = {
            "client_id": self.client_id,
            "trained_at": datetime.now().isoformat(),
            "data_version": data_version,
            "data_source": data_source,
            "n_samples": len(X),
            "n_features": len(X.columns),
            "feature_names": self.feature_names_,
            "target_mean": float(y.mean()),
            "target_std": float(y.std()),
            "simulator_version": self.simulator_version
        }

        self.fitted_ = True
        self.status = ModelStatus.TRAINED

        return self

    # --------------------------------------------------------

    def predict(self, X: pd.DataFrame) -> Dict[str, np.ndarray]:

        if not self.fitted_:
            raise RuntimeError("Model not fitted.")

        if list(X.columns) != self.feature_names_:
            raise ValueError("Feature mismatch detected.")

        predictions = {}

        for alpha, model in self.models.items():
            key = f"p{int(alpha * 100)}"
            predictions[key] = model.predict(X)

        return predictions

    # --------------------------------------------------------

    def deploy(self):
        if self.status != ModelStatus.TRAINED:
            raise RuntimeError("Only trained models can be deployed.")

        self.status = ModelStatus.DEPLOYED
        self.deployed_at = datetime.now()

    # --------------------------------------------------------

    def retire(self):
        self.status = ModelStatus.RETIRED
        self.retired_at = datetime.now()

    # --------------------------------------------------------

    def save(self, filepath: str):

        if not self.fitted_:
            raise RuntimeError("Cannot save unfitted model.")

        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        save_obj = {
            "client_id": self.client_id,
            "status": self.status.value,
            "deployed_at": self.deployed_at.isoformat() if self.deployed_at else None,
            "retired_at": self.retired_at.isoformat() if self.retired_at else None,
            "data_version": self.data_version,
            "data_source": self.data_source,
            "models": self.models,
            "feature_names": self.feature_names_,
            "training_metadata": self.training_metadata_,
            "simulator_version": self.simulator_version
        }

        joblib.dump(save_obj, filepath)
        print(f"Model saved to {filepath}")

    # --------------------------------------------------------

    @classmethod
    def load(cls, filepath: str) -> "QuantileEnsemble":

        save_obj = joblib.load(filepath)

        instance = cls(
            client_id=save_obj["client_id"],
            simulator_version=save_obj.get("simulator_version", "unknown")
        )

        instance.models = save_obj["models"]
        instance.feature_names_ = save_obj["feature_names"]
        instance.training_metadata_ = save_obj["training_metadata"]
        instance.data_version = save_obj.get("data_version")
        instance.data_source = save_obj.get("data_source")
        instance.status = ModelStatus(save_obj["status"])
        instance.fitted_ = True

        return instance
