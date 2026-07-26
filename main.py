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
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import ModelTrainerConfig  

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

        logging.info("Model Training Started")
        model_trainer_config = ModelTrainerConfig(training_pipeline_config)  # ← FIXED
        model_trainer = ModelTrainer(
            model_trainer_config=model_trainer_config,
            data_transformation_artifact=data_transformation_artifact
        )
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info("Model Training Artifact created.")
        
        # print("\n" + "="*50)
        # print("📊 MODEL PERFORMANCE METRICS")
        # print("="*50)

        # # Train metrics
        # print("\n🔹 TRAIN SET:")
        # print(f"   F1 Score:     {model_trainer_artifact.train_metric_artifact.f1_score:.4f}")
        # print(f"   Precision:    {model_trainer_artifact.train_metric_artifact.precision_score:.4f}")
        # print(f"   Recall:       {model_trainer_artifact.train_metric_artifact.recall_score:.4f}")

        # # Test metrics
        # print("\n🔹 TEST SET:")
        # print(f"   F1 Score:     {model_trainer_artifact.test_metric_artifact.f1_score:.4f}")
        # print(f"   Precision:    {model_trainer_artifact.test_metric_artifact.precision_score:.4f}")
        # print(f"   Recall:       {model_trainer_artifact.test_metric_artifact.recall_score:.4f}")

        # # Check if model meets expected accuracy
        # if model_trainer_artifact.test_metric_artifact.f1_score >= 0.6:
        #     print("\n✅ Model meets expected accuracy threshold (>= 0.6)")
        # else:
        #     print("\n⚠️ Model below expected accuracy threshold (< 0.6)")

    except Exception as e:
        raise NetworkSecurityException(e, sys) from e