from dataclasses import dataclass
import os

from src.exception import CustomException
from src.logger import logging
from src import utils

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBRegressor

from sklearn.base import BaseEstimator
from sklearn.metrics import r2_score

@dataclass
class ModelTrainerConfig:
    model_path: str = os.path.join("artifacts", "model.pkl")
    models = [
        ("Linear Regression", LinearRegression(), {}),

        ("Ridge Regression", Ridge(), {
            "alpha": [0.01, 0.1, 1.0, 10.0, 100.0],
            "solver": ["auto", "svd", "cholesky", "lsqr"]
        }),

        ("Decision Tree", DecisionTreeRegressor(), {
            "max_depth": [None, 5, 10, 20],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4],
            "criterion": ["squared_error", "friedman_mse"]
        }),

        ("Random Forest", RandomForestRegressor(), {
            "n_estimators": [100, 200, 500],
            "max_depth": [None, 10, 20, 50],
            "min_samples_leaf": [1, 2, 4],
        }),

        ("Gradient Boost", GradientBoostingRegressor(), {
            "n_estimators": [100, 200],
            "learning_rate": [0.01, 0.1, 0.2],
            "max_depth": [3, 5, 10],
            "min_samples_split": [2, 5],
        }),

        ("K Nearest Neighbours", KNeighborsRegressor(), {
            "n_neighbors": [3, 5, 7, 9],
            "weights": ["uniform", "distance"],
            "algorithm": ["auto", "ball_tree", "kd_tree"],
        }),

        ("Support vector", SVR(), {
            "kernel": ["linear", "rbf", "poly"],
            "C": [0.1, 1, 10],
            "epsilon": [0.01, 0.1, 0.2],
            "gamma": ["scale", "auto"]
        }),

        ("Naive Bayes", GaussianNB(), {}),

        ("Xg Boost", XGBRegressor(objective='reg:squarederror'), {
            "n_estimators": [100, 200, 300],
            "learning_rate": [0.01, 0.1, 0.2],
            "max_depth": [3, 5, 7],
            "subsample": [0.7, 0.8, 1.0],
            "colsample_bytree": [0.7, 0.8, 1.0]
        })
    ]


class ModelTrainer:
    def __init__(self):
        self.config = ModelTrainerConfig()

    def train_models(self, X_train, X_test, y_train, y_test):
        """
        Trains a list of models. Finds the top 3 models and
        does hyperparamter tuning.
        Saves the model with highest accuracy.

        Returns: model, model_file_path, r2_score
        """
        try:
            top_models = utils.top_n_models(X_train, X_test, y_train, y_test, self.config.models, 3)
            model: BaseEstimator
            model, params, _ = utils.tune_models(X_train, y_train, top_models)

            model.set_params(**params)
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)
            r2 = r2_score(y_true=y_test, y_pred=y_pred)
            logging.info(f"Best model: [{model}], Best score: [{r2}]")

            utils.save_object(model, self.config.model_path)
            return model, self.config.model_path, r2
        
        except Exception as e:
            raise CustomException("model trainer", e)
