import mlflow
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import os
import warnings
import sys

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    np.random.seed(40)

    file_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "train_pca.csv")
    data = pd.read_csv(file_path)

    X_train, X_test, y_train, y_test = train_test_split(
        data.drop("Credit_Score", axis=1),
        data["Credit_Score"],
        random_state=42,
        test_size=0.2
    )
    input_example = X_train[0:5]

    # 🔹 Hyperparameter grid (bisa kamu atur sesuai kebutuhan)
    n_estimators_list = [100, 200, 300, 400, 500]
    max_depth_list = [5, 10, 20, 30, 40]

    for n_estimators in n_estimators_list:
        for max_depth in max_depth_list:
            with mlflow.start_run():
                model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
                model.fit(X_train, y_train)

                accuracy = model.score(X_test, y_test)

                # Log params & metrics
                mlflow.log_param("n_estimators", n_estimators)
                mlflow.log_param("max_depth", max_depth)
                mlflow.log_metric("accuracy", accuracy)

                # Log model
                mlflow.sklearn.log_model(
                    sk_model=model,
                    artifact_path="model",
                    input_example=input_example
                )
