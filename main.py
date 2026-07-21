from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import (
    DataIngestionConfig,
    TrainingPipelineConfig
)
import sys


if __name__ == "__main__":
    try:
        # 1. Create main training pipeline configuration
        training_pipeline_config = TrainingPipelineConfig()

        # 2. Create data ingestion configuration
        data_ingestion_config = DataIngestionConfig(
            training_pipeline_config
        )

        # 3. Create DataIngestion object
        data_ingestion = DataIngestion(
            data_ingestion_config
        )

        logging.info("Initiating the data ingestion")

        # 4. Run the complete data ingestion process
        data_ingestion_artifact = (
            data_ingestion.initiate_data_ingestion()
        )

        # 5. Print paths of generated train/test files
        print(data_ingestion_artifact)

    except Exception as e:
        raise NetworkSecurityException(e, sys)