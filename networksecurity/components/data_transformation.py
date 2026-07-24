import os
import sys
import numpy as np
import pandas as pd

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import (
    TARGET_COLUMN,
    DATA_TRANSFORMATION_IMPUTER_PARAMS
)

from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)

from networksecurity.entity.config_entity import (
    DataTransformationConfig
)

from networksecurity.exception.exception import (
    NetworkSecurityException
)

from networksecurity.logging.logger import logging

from networksecurity.utils.main_utils.utils import (
    save_numpy_array_data,
    save_object
)


class DataTransformation:

    def __init__(
        self,
        data_validation_artifact: DataValidationArtifact,
        data_transformation_config: DataTransformationConfig,
    ):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        """
        Reads CSV file and returns DataFrame.
        """
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    @staticmethod
    def get_data_transformer_object() -> Pipeline:
        """
        Creates preprocessing pipeline.
        """
        try:
            logging.info("Creating KNN Imputer")

            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)

            preprocessor = Pipeline(
                steps=[
                    ("imputer", imputer)
                ]
            )

            logging.info("Pipeline created successfully")

            return preprocessor

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """
        Performs data transformation and returns DataTransformationArtifact.
        """

        logging.info("Entered Data Transformation")

        try:

            # Read validated datasets
            train_df = self.read_data(
                self.data_validation_artifact.valid_train_file_path
            )

            test_df = self.read_data(
                self.data_validation_artifact.valid_test_file_path
            )

            # Training Data
            input_feature_train_df = train_df.drop(
                columns=[TARGET_COLUMN],
                axis=1
            )

            target_feature_train_df = train_df[TARGET_COLUMN].replace(-1, 0)

            # Testing Data
            input_feature_test_df = test_df.drop(
                columns=[TARGET_COLUMN],
                axis=1
            )

            target_feature_test_df = test_df[TARGET_COLUMN].replace(-1, 0)

            # Create preprocessing object
            preprocessing_obj = self.get_data_transformer_object()

            # Fit & Transform training data
            input_feature_train_arr = preprocessing_obj.fit_transform(
                input_feature_train_df
            )

            # Transform testing data
            input_feature_test_arr = preprocessing_obj.transform(
                input_feature_test_df
            )

            # Combine X and y
            train_arr = np.c_[
                input_feature_train_arr,
                np.array(target_feature_train_df)
            ]

            test_arr = np.c_[
                input_feature_test_arr,
                np.array(target_feature_test_df)
            ]

            # Create output directory if not exists
            os.makedirs(
                os.path.dirname(
                    self.data_transformation_config.transformed_train_file_path
                ),
                exist_ok=True,
            )

            # Save transformed arrays
            save_numpy_array_data(
                self.data_transformation_config.transformed_train_file_path,
                train_arr,
            )

            save_numpy_array_data(
                self.data_transformation_config.transformed_test_file_path,
                test_arr,
            )

            # Save preprocessing object
            save_object(
                self.data_transformation_config.transformed_object_file_path,
                preprocessing_obj,
            )

            # Create artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                preprocessor_object_file_path=self.data_transformation_config.transformed_object_file_path,
            )

            logging.info("Data Transformation completed successfully")

            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e