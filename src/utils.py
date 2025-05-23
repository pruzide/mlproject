import os
import sys
import pandas as pd
import numpy as np
from src.exception import CustomException
from src.logger import logging
import dill
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

def save_object(file_path,obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok = True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj,file_obj)


    except Exception as e:
        raise CustomException(e,sys)
    
def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]

            para=param[list(models.keys())[i]] ## list(model.keys())[i] will give name of algorithm and we have created param dictionary in such a way so that by accessing the name of the algorithm we can access the respective parameters to test out in gridsearchCV to find out the best parameters

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_) ## ** unpacks dictionary so that set_params() method received keyword arguments and not a dictionary 
            model.fit(X_train,y_train)   ## gs.best_params_ gives a dictionary contating best params

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

             # Print the R² scores
            print(f"{list(models.keys())[i]}: Train R² = {train_model_score:.4f}, Test R² = {test_model_score:.4f}")  ## .4f is to control the number of decimal places to show in the output to not overcrowd the terminal space 

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)
    
def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)