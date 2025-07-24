from dataclasses import dataclass
import os
import pandas as pd

from src.exception import CustomException
from src.logger import logging
from src import utils

@dataclass
class DataFormat:
    gender: str
    race_ethnicity: str
    parental_level_of_education: str
    lunch: str
    test_preparation_course: str
    reading_score: float
    writing_score: float

    def get_frame(self):
        logging.info("Preparing prediction dataframe")
        return pd.DataFrame({
            "gender": [self.gender],
            "race_ethnicity": [self.race_ethnicity],
            "parental_level_of_education": [self.parental_level_of_education],
            "lunch": [self.lunch],
            "test_preparation_course": [self.test_preparation_course],
            "reading_score": [self.reading_score],
            "writing_score": [self.writing_score]
        })

class PredictionPipeline:
    def predict(prediction_data: DataFormat):
        try:
            model_path = os.path.join("artifacts", "model.pkl")
            preprocessor_path = os.path.join("artifacts", "preprocessor.pkl")

            model = utils.load_object(path=model_path)
            preprocessor = utils.load_object(path=preprocessor_path)

            logging.info(f"Initiating prediction for [{prediction_data}]")
            data_transformed = preprocessor.transform(prediction_data.get_frame())
            prediction = model.predict(data_transformed)
            logging.info(f"Prediction result: [{prediction[0]}]")

            return prediction[0]
        except Exception as e:
            raise CustomException("data prediction", e)