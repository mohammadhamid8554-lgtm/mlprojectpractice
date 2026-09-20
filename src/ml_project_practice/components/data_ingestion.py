from dataclasses import dataclass
import os
import sys
from typing import Optional

# pandas loads the dataset, while train_test_split creates train/test subsets.
import pandas as pd
from sklearn.model_selection import train_test_split

# Project-wide logging and readable exception handling keep failures easy to trace.
from src.ml_project_practice.logger import logging
from src.ml_project_practice.exception import CustomException
from src.ml_project_practice.utils import read_sql_data


@dataclass
class DataIngestionConfig:
    """Store the file paths produced during data ingestion."""

    raw_data_path: str = os.path.join("artifacts", "raw.csv")
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")


class DataIngestion:
    """Load the raw dataset, split it, and save train/test files."""

    def __init__(self, config: Optional[DataIngestionConfig] = None):
        # Use a custom configuration when provided; otherwise use project defaults.
        self.ingestion_config = config or DataIngestionConfig()

    def initiate_data_ingestion(self) -> tuple[str, str]:
        try:
            # Load the source dataset from MySQL before creating train/test files.
            df = read_sql_data()

            logging.info("Data loaded successfully.")

            # Ensure the output folder exists before writing any artifacts.
            os.makedirs(
                os.path.dirname(self.ingestion_config.raw_data_path),
                exist_ok=True,
            )
            df.to_csv(self.ingestion_config.raw_data_path, index=False)

            # Keep 80% for training and 20% for evaluating the trained model.
            train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

            train_df.to_csv(self.ingestion_config.train_data_path, index=False)
            test_df.to_csv(self.ingestion_config.test_data_path, index=False)

            logging.info("Train/Test split completed successfully.")
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )

        except Exception as error:
            # Wrap the original error with the file and line that caused it.
            raise CustomException(error, sys) from error
        

