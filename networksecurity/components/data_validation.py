from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact
)
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import (
    read_yaml_file,
    write_yaml_file
)

import os
import sys
import pandas as pd
from scipy.stats import ks_2samp


class DataValidation:

    def __init__(
        self,
        data_ingestion_artifect: DataIngestionArtifact,
        data_validation_config: DataValidationConfig
    ):
        try:
            self.data_ingestion_artifect = data_ingestion_artifect
            self.data_validation_config = data_validation_config

            # Read schema.yaml
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


    # -------------------------------------------------
    # Validate Number of Columns
    # -------------------------------------------------
    def validate_number_of_columns(
        self,
        dataframe: pd.DataFrame
    ) -> bool:

        try:
            # Get expected number of columns from schema.yaml
            number_of_columns = len(
                self._schema_config["columns"]
            )

            logging.info(
                f"Required number of columns: {number_of_columns}"
            )

            logging.info(
                f"Dataframe columns: {len(dataframe.columns)}"
            )

            if len(dataframe.columns) == number_of_columns:
                return True

            return False

        except Exception as e:
            raise NetworkSecurityException(e, sys)


    # -------------------------------------------------
    # Validate Numerical Columns
    # -------------------------------------------------
    def validate_numerical_columns(
        self,
        dataframe: pd.DataFrame
    ) -> bool:

        try:
            # Get numerical columns from schema.yaml
            numerical_columns = self._schema_config[
                "numerical_columns"
            ]

            dataframe_columns = dataframe.columns

            # Check every numerical column
            for column in numerical_columns:

                if column not in dataframe_columns:

                    logging.error(
                        f"Numerical column missing: {column}"
                    )

                    return False

            logging.info(
                "All numerical columns are present in the dataframe."
            )

            return True

        except Exception as e:
            raise NetworkSecurityException(e, sys)


    # -------------------------------------------------
    # Read CSV Data
    # -------------------------------------------------
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:

        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


    # -------------------------------------------------
    # Detect Dataset Drift
    # -------------------------------------------------
    def detect_dataset_drift(
        self,
        base_df: pd.DataFrame,
        current_df: pd.DataFrame,
        threshold: float = 0.05
    ) -> bool:

        try:
            # Initially assume there is no drift
            status = True

            # Dictionary for storing drift results
            report = {}

            # Check drift column by column
            for column in base_df.columns:

                # Base/reference data
                d1 = base_df[column]

                # Current/comparison data
                d2 = current_df[column]

                # Perform KS Test
                ks_test_result = ks_2samp(d1, d2)

                p_value = ks_test_result.pvalue

                # Check for drift
                if p_value >= threshold:

                    # No drift
                    is_found = False

                else:

                    # Drift found
                    is_found = True

                    # Overall validation status becomes False
                    status = False

                # Add result to report
                report.update({
                    column: {
                        "pvalue": float(p_value),
                        "drift_status": is_found
                    }
                })

            # Get drift report file path
            drift_report_file_path = (
                self.data_validation_config
                .drift_report_file_path
            )

            # Save complete drift report
            write_yaml_file(
                file_path=drift_report_file_path,
                content=report,
                replace=True
            )

            logging.info(
                f"Data drift report saved at: "
                f"{drift_report_file_path}"
            )

            return status

        except Exception as e:
            raise NetworkSecurityException(e, sys)


    # -------------------------------------------------
    # Initiate Data Validation
    # -------------------------------------------------
    def initiate_data_validation(
        self
    ) -> DataValidationArtifact:

        try:
            logging.info(
                "Starting data validation"
            )

            # -----------------------------------------
            # Get Train and Test File Paths
            # -----------------------------------------

            train_file_path = (
                self.data_ingestion_artifect
                .trained_file_path
            )

            test_file_path = (
                self.data_ingestion_artifect
                .test_file_path
            )


            # -----------------------------------------
            # Read Train and Test Data
            # -----------------------------------------

            train_dataframe = DataValidation.read_data(
                train_file_path
            )

            test_dataframe = DataValidation.read_data(
                test_file_path
            )


            # -----------------------------------------
            # Validate Number of Columns
            # -----------------------------------------

            status = self.validate_number_of_columns(
                train_dataframe
            )

            if not status:
                raise Exception(
                    "Number of columns not matched "
                    "in train file."
                )


            status = self.validate_number_of_columns(
                test_dataframe
            )

            if not status:
                raise Exception(
                    "Number of columns not matched "
                    "in test file."
                )


            # -----------------------------------------
            # Validate Numerical Columns
            # -----------------------------------------

            status = self.validate_numerical_columns(
                train_dataframe
            )

            if not status:
                raise Exception(
                    "Required numerical columns "
                    "are missing in train file."
                )


            status = self.validate_numerical_columns(
                test_dataframe
            )

            if not status:
                raise Exception(
                    "Required numerical columns "
                    "are missing in test file."
                )


            # -----------------------------------------
            # Detect Data Drift
            # -----------------------------------------

            status = self.detect_dataset_drift(
                base_df=train_dataframe,
                current_df=test_dataframe
            )


            # -----------------------------------------
            # Create Valid Data Directory
            # -----------------------------------------

            valid_data_dir = os.path.dirname(
                self.data_validation_config
                .valid_train_file_path
            )

            os.makedirs(
                valid_data_dir,
                exist_ok=True
            )


            # -----------------------------------------
            # Save Valid Train Data
            # -----------------------------------------

            train_dataframe.to_csv(
                self.data_validation_config
                .valid_train_file_path,
                index=False
            )


            # -----------------------------------------
            # Save Valid Test Data
            # -----------------------------------------

            test_dataframe.to_csv(
                self.data_validation_config
                .valid_test_file_path,
                index=False
            )


            # -----------------------------------------
            # Create Data Validation Artifact
            # -----------------------------------------

            data_validation_artifact = (
                DataValidationArtifact(

                    validation_status=status,

                    valid_train_file_path=(
                        self.data_validation_config
                        .valid_train_file_path
                    ),

                    valid_test_file_path=(
                        self.data_validation_config
                        .valid_test_file_path
                    ),

                    invalid_train_file_path=(
                        self.data_validation_config
                        .invalid_train_file_path
                    ),

                    invalid_test_file_path=(
                        self.data_validation_config
                        .invalid_test_file_path
                    ),

                    drift_report_file_path=(
                        self.data_validation_config
                        .drift_report_file_path
                    )
                )
            )

            logging.info(
                f"Data Validation Artifact: "
                f"{data_validation_artifact}"
            )

            # IMPORTANT: Return artifact
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)