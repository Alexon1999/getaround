from mlflow.models.signature import infer_signature
import time
import mlflow
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
import warnings
import joblib

warnings.filterwarnings('ignore')

if __name__ == "__main__":

    # ### Tracking model with MLFlow

    # Set your variables for your environment
    EXPERIMENT_NAME = "getaround"

    # Set experiment's info
    mlflow.set_experiment(EXPERIMENT_NAME)
    # Get our experiment info
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

    print("training model...")

    # Time execution
    start_time = time.time()

    # Call mlflow autolog
    mlflow.sklearn.autolog(log_models=False)  # We won't log models right away

    df = pd.read_csv('get_around_pricing_project.csv', index_col=0)

    # ## X, Y split

    # Extract the features
    X = df.drop('rental_price_per_day', axis=1)

    # Extract the target column
    y = df.loc[:, 'rental_price_per_day']

    # Train / test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, random_state=42, test_size=0.2)

    # ## Preprocessing

    # determine categorical and numerical features
    numerical_features = X.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = X.select_dtypes(include=['object', 'bool']).columns

    # Numerical Transformer
    numerical_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])

    # Categorical Transformer
    categorical_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(drop='first', handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("numerical_transformer", numerical_transformer, numerical_features),
            ("categorical_transformer", categorical_transformer, categorical_features)
        ]
    )

    # ## Build Model

    # Pipeline Model
    model = Pipeline(
        steps=[
            ("preprocessing", preprocessor),
            ("Regressor", RandomForestRegressor(
                max_features='sqrt', min_samples_leaf=1, n_estimators=300))
        ]
    )

    # Log experiment to MLFlow
    with mlflow.start_run(experiment_id=experiment.experiment_id):
        model.fit(X_train, y_train)
        predictions = model.predict(X_train)

        mlflow.log_metric("Train Score", model.score(X_train, y_train))
        mlflow.log_metric("Test Score", model.score(X_test, y_test))

        # Log model seperately to have more flexibility on setup
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="getaround-optimum-prices",
            registered_model_name="random_forest_regressor",
            signature=infer_signature(X_train, predictions)
        )

    print("...Done!")
    print(f"---Total training time: {time.time()-start_time}")
