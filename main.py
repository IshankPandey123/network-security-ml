import sys

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation

from networksecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig
)

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


if __name__ == "__main__":
    try:

        # ======================================
        # Training Pipeline Configuration
        # ======================================
        training_pipeline_config = TrainingPipelineConfig()

        # ======================================
        # Data Ingestion
        # ======================================
        logging.info("Starting Data Ingestion")

        data_ingestion_config = DataIngestionConfig(
            training_pipeline_config
        )

        data_ingestion = DataIngestion(
            data_ingestion_config
        )

        data_ingestion_artifact = (
            data_ingestion.initiate_data_ingestion()
        )

        print(data_ingestion_artifact)

        logging.info("Data Ingestion Completed Successfully")

        # ======================================
        # Data Validation
        # ======================================
        logging.info("Starting Data Validation")

        data_validation_config = DataValidationConfig(
            training_pipeline_config
        )

        data_validation = DataValidation(
            data_ingestion_artifact,
            data_validation_config
        )

        data_validation_artifact = (
            data_validation.initiate_data_validation()
        )

        print(data_validation_artifact)

        logging.info("Data Validation Completed Successfully")

        # ======================================
        # Data Transformation
        # ======================================
        logging.info("Starting Data Transformation")

        data_transformation_config = DataTransformationConfig(
            training_pipeline_config
        )

        data_transformation = DataTransformation(
            data_validation_artifact,
            data_transformation_config
        )

        data_transformation_artifact = (
            data_transformation.initiate_data_transformation()
        )

        print(data_transformation_artifact)

        logging.info("Data Transformation Completed Successfully")

    except Exception as e:
        raise NetworkSecurityException(e, sys) from e