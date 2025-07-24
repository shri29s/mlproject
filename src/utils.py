import os
import dill
import numpy as np

from src.exception import CustomException
from src.logger import logging

from sklearn.metrics import r2_score
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn.base import BaseEstimator

# Some parameters
N_ITER = 10

def save_object(obj, path):
    try:
        dir = os.path.dirname(path)
        os.makedirs(dir, exist_ok=True)

        with open(path, "wb") as file:
            dill.dump(obj=obj, file=file)
        logging.info(f"Saved object at [{path}]")

    except Exception as e:
        raise CustomException(location="save object", e=e)
    
def load_object(path):
    try:
        with open(path, "rb") as file:
            obj = dill.load(file=file)
        logging.info(f"Loaded object from [{path}]")
        return obj
    except Exception as e:
        raise CustomException(location="load object", e=e)
    
def evaluate_model(X_train, X_test, y_train, y_test, model_tuple):
    try:
        logging.info(f"Evaluating model: [{model_tuple[0]}]")
        model = model_tuple[1]
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        logging.info(f"R2 score of [{model_tuple[0]}] is [{r2}]")
        return r2
    except Exception as e:
        raise CustomException(location="evaluate model", e=e)

def top_n_models(X_train, X_test, y_train, y_test, model_list, n):
    try:
        r2_scores = []
        logging.info("Initiating model evaluation")
        for model_tuple in model_list:
            r2 = evaluate_model(X_train, X_test, y_train, y_test, model_tuple)
            r2_scores.append((model_tuple, r2))

        r2_scores.sort(key=lambda x: x[1], reverse=True)
        r2_scores = r2_scores[:n]
        logging.info(f"Seperating out top [{n}] models")

        top_models = []
        for i in r2_scores:
            top_models.append(i[0])
        return top_models
    except Exception as e:
        raise CustomException(location="top models finder", e=e)

def tune_single_model(X_train, y_train, model_tuple):
    try:
        model: BaseEstimator = model_tuple[1]
        params = model_tuple[2]

        total_combinations = np.prod([len(v) for v in params.values()])  
        if total_combinations < N_ITER:
            logging.info(f"Tuning model: [{model_tuple[0]}] with GridSearchCV")
            grid_cv = GridSearchCV(
                estimator=model,
                param_grid=params,
                scoring="r2",
                n_jobs=-1
            )

            grid_cv.fit(X_train, y_train)
            return grid_cv.best_params_, grid_cv.best_score_
        else:
            logging.info(f"Tuning model: [{model_tuple[0]}] with RandomizedSearchCV")
            rand_cv = RandomizedSearchCV(
                estimator=model, 
                param_distributions=params, 
                scoring="r2", 
                n_jobs=-1,
                n_iter=N_ITER
            )

            rand_cv.fit(X_train, y_train)
            return rand_cv.best_params_, rand_cv.best_score_
    except Exception as e:
        raise CustomException("single model tuner", e)

def tune_models(X_train, y_train, model_list):
    """
    Returns: model, best_params, best_score
    """
    try:
        models_data = []
        logging.info("Initiating hyperparameter tuning")
        for model_tuple in model_list:
            param, score = tune_single_model(X_train, y_train, model_tuple)
            models_data.append((model_tuple, param, score))

        best_model = max(*models_data, key=lambda x: x[2])
        logging.info(f"Best model found: [{best_model[0][1]}] parameters: [{best_model[1]}], with best score: [{best_model[2]}]")
        return best_model[0][1], best_model[1], best_model[2]
    except Exception as e:
        raise CustomException("multiple model tuner", e)