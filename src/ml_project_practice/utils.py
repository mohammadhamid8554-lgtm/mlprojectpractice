import os
import pickle
import sys
from typing import Any

import pandas as pd
from dotenv import load_dotenv
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import GridSearchCV

from .exception import CustomException
from .logger import logger


load_dotenv()


def read_sql_data():
    """Read the quality table from MySQL."""
    logger.info("Reading SQL database started.")

    try:
        import pymysql

        host = os.getenv("host")
        user = os.getenv("user")
        password = os.getenv("password")
        db = os.getenv("db")

        if any(value is None for value in (host, user, password, db)):
            raise ValueError("Database environment variables are incomplete")

        assert host is not None
        assert user is not None
        assert password is not None
        assert db is not None

        # Open the database connection only after all required settings are ready.
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db,
        )
        logger.info("Database connection established.")

        # Keep the SQL query in one place so the source table is easy to change.
        df = pd.read_sql_query(
            "SELECT * FROM quality",
            connection,  # pyright: ignore[reportArgumentType]
        )
        connection.close()
        logger.info("SQL data loaded successfully.")
        return df
    except Exception as e:
        logger.error("Error while reading SQL data: %s", e)
        raise CustomException(e, sys) from e


def evaluate_classification_models(
    X_train: Any,
    X_test: Any,
    y_train: Any,
    y_test: Any,
    models: dict[str, Any],
    parameters: dict[str, dict[str, list[Any]]],
    scoring: str = "f1_weighted",
) -> tuple[Any, dict[str, dict[str, float]]]:
    """Tune classifiers, compare their metrics, and return the best model.

    The model with the highest test-set F1 score is selected. Weighted F1 is
    suitable when the target classes are not perfectly balanced.
    """
    try:
        if not models:
            raise ValueError("At least one classification model is required.")

        # Store the scores for every model so they can be compared later.
        model_report: dict[str, dict[str, float]] = {}
        best_model = None
        best_score = float("-inf")

        for model_name, model in models.items():
            # Search for the best hyperparameters without looking at test data.
            grid_search = GridSearchCV(
                estimator=model,
                param_grid=parameters.get(model_name, {}),
                scoring=scoring,
                cv=3,
                n_jobs=-1,
            )
            grid_search.fit(X_train, y_train)

            # Grid search returns the best already-fitted version of this model.
            candidate_model = grid_search.best_estimator_
            predictions = candidate_model.predict(X_test)

            # Calculate several useful metrics instead of judging the model by
            # accuracy alone, especially when the classes are imbalanced.
            accuracy = accuracy_score(y_test, predictions)
            precision = precision_score(
                y_test,
                predictions,
                average="weighted",
                zero_division=0,
            )
            recall = recall_score(
                y_test,
                predictions,
                average="weighted",
                zero_division=0,
            )
            f1 = f1_score(
                y_test,
                predictions,
                average="weighted",
                zero_division=0,
            )

            model_report[model_name] = {
                "accuracy": float(accuracy),
                "precision": float(precision),
                "recall": float(recall),
                "f1_score": float(f1),
            }
            logger.info(
                "Model: %s | Accuracy: %.4f | F1: %.4f",
                model_name,
                accuracy,
                f1,
            )

            # Weighted F1 is the selection metric for this project.
            if f1 > best_score:
                best_score = f1
                best_model = candidate_model

        if best_model is None:
            raise ValueError("No classification model could be trained.")

        logger.info("Best classification model selected with F1: %.4f", best_score)
        return best_model, model_report

    except Exception as error:
        logger.error("Error while evaluating classification models: %s", error)
        raise CustomException(error, sys) from error
