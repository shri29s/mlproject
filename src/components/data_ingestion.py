import os
import pandas as pd

from src.exception import CustomException
from src.logger import logging

from sklearn.model_selection import train_test_split

from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join("artifacts", "data.csv")
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")

class DataIngestion:
    def __init__(self):
        self.config = DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        try:
            logging.info("Data ingestion started")
            df = pd.read_csv(r"notebooks/data/stud.csv")

            os.makedirs(os.path.dirname(self.config.train_data_path), exist_ok=True)
            df.to_csv(self.config.raw_data_path, index=False, header=True)

            df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)
            logging.info("Splitted train and test data")

            df_train.to_csv(self.config.train_data_path, index=False, header=True)
            df_test.to_csv(self.config.test_data_path, index=False, header=True)
            logging.info(f"Data stored in [{os.path.dirname(self.config.train_data_path)}] directory")
        except Exception as e:
            raise CustomException("Error in data ingestion stage: " + str(e))


# if __name__=="__main__":
#     data_ingestion = DataIngestion()
#     data_ingestion.initiate_data_ingestion()