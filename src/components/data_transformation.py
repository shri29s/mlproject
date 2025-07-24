from dataclasses import dataclass
import os

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from src.exception import CustomException
from src.logger import logging
from src import utils

@dataclass
class DataTransformationConfig:
    preprocessor_path: str = os.path.join("artifacts", "preprocessor.pkl")
    target_column: str = "math_score"


class DataTransformer:
    def __init__(self):
        self.config = DataTransformationConfig()

    def get_preprocessor(self):
        try:
            numerical_columns = ['reading_score', 'writing_score']
            categorical_columns = ['gender', 'race_ethnicity', 
                                'parental_level_of_education', 
                                'lunch', 'test_preparation_course']
            
            logging.info("Setting up numerical and categorical pipelines")

            numerical_pipeline = Pipeline(steps=[
                ("impute", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler())
            ])

            categorical_pipeline = Pipeline(steps=[
                ("impute", SimpleImputer(strategy="most_frequent")),
                ("ohe", OneHotEncoder(drop="first"))
            ])

            logging.info("Setting up the main preprocessor")
            preprocessor = ColumnTransformer([
                ("numerical", numerical_pipeline, numerical_columns),
                ("categorical", categorical_pipeline, categorical_columns)
            ])

            return preprocessor
        except Exception as e:
            raise CustomException(location="preprocesser", e=e)
    
    def transform(self, train_data: pd.DataFrame, test_data: pd.DataFrame):
        '''
        This function gets the preprocesser, seperate the X and y
        and then transform the independent columns.
        Returns transformed: X_train, X_test, y_train, y_test
        '''
        try:
            preprocessor = self.get_preprocessor()

            logging.info("Splitting data into X and y")
            X_train = train_data.drop(self.config.target_column, axis=1)
            X_test = test_data.drop(self.config.target_column, axis=1)

            y_train = train_data[self.config.target_column]
            y_test = test_data[self.config.target_column]

            logging.info("Transforming X_train and X_test")

            X_train_transformed = preprocessor.fit_transform(X_train)
            X_test_transformed = preprocessor.transform(X_test)

            utils.save_object(preprocessor, self.config.preprocessor_path)
            return X_train_transformed, X_test_transformed, y_train, y_test
        
        except Exception as e:
            raise CustomException("data transformer", e)