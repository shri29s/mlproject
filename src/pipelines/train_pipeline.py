from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformer
from src.components.model_trainer import ModelTrainer

from src.exception import CustomException
from src.logger import logging

class TrainPipeline:
    def execute_training():
        try:
            logging.info("Executing training pipeline")
            data_ingestion = DataIngestion()
            df_train, df_test = data_ingestion.data_ingestion()

            data_transformer = DataTransformer()
            X_train, X_test, y_train, y_test = data_transformer.transform(df_train, df_test)

            trainer = ModelTrainer()
            trainer.train_models(X_train, X_test, y_train, y_test)
            logging.info("Model training successful")
            
        except Exception as e:
            raise CustomException("train pipeline", e)
        
if __name__=="__main__":
    TrainPipeline.execute_training()