import os
import dill

from src.exception import CustomException
from src.logger import logging

def save_object(obj, path):
    try:
        dir = os.path.dirname(path)
        os.makedirs(dir, exist_ok=True)

        with open(path, "wb") as file:
            dill.dump(obj=obj, file=file)
        logging.info(f"Saved object at [{path}]")

    except Exception as e:
        raise CustomException(location="save object", e=e)