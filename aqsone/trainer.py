from aqsone.data import get_data, clean_df, holdout
from aqsone.model import get_model
from aqsone.pipeline import get_pipeline
from aqsone.metrics import compute_rmse
from aqsone.mlflow import MLFlowBase

import joblib


class Trainer(MLFlowBase):
    def __init__(self):
        super().__init__("[FR] [AQSONE] [galleon] test 👋", "https://mlflow.lewagon.co")

    def train(self):

        model_name = "random_forest"
        line_count = 1_000

        # get data
        df = get_data(line_count)
        df = clean_df(df)

        # holdout
        X_train, X_test, y_train, y_test = holdout(df)

        # create model
        model = get_model(model_name)

        # create pipeline
        pipeline = get_pipeline(model)

        # train
        pipeline.fit(X_train, y_train)

        # make prediction for metrics
        y_pred = pipeline.predict(X_test)

        # evaluate metrics
        rmse = compute_rmse(y_pred, y_test)

        # save the trained model
        joblib.dump(pipeline, f"model_{model_name}_{line_count}.joblib")

        # return the pipeline in order to identify the best estimators and params
        return pipeline
