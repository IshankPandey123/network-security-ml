# 🔐 Network Security Threat Detection using Machine Learning

## 📌 Overview

**Network Security Threat Detection** is an end-to-end Machine Learning project designed to identify whether network traffic is **malicious or normal**.

The project implements a **production-ready ML pipeline** following industry-standard MLOps practices:

![alt text](image-1.png)

---

## 🚀 Key Features

This project follows modern **Machine Learning Engineering principles**:

- 🏗️ **Modular Pipeline Architecture**  
  Structured workflow for scalable ML development and deployment.

- ✅ **Data Validation**  
  Ensures data quality, consistency, and schema correctness before training.

- 📊 **Dataset Drift Detection**  
  Detects changes between training and incoming data distributions.

- 🤖 **Automated Model Training**  
  Complete pipeline for preprocessing, training, evaluation, and model saving.

- 📈 **MLflow Experiment Tracking**  
  Tracks experiments, metrics, parameters, and model versions.

- ⚡ **FastAPI Deployment**  
  Provides a lightweight REST API for real-time predictions.

- 📦 **Batch Prediction Pipeline**  
  Supports large-scale prediction on new network data.

---

## 🛠️ Technology Stack

| Category | Technologies |
|----------|-------------|
| Programming Language | Python |
| Machine Learning | Scikit-learn |
| API Framework | FastAPI |
| Experiment Tracking | MLflow |
| Database | MongoDB |
| Deployment | Docker, AWS |
| Data Processing | Pandas, NumPy |

---

## 🎯 Problem Statement

With the rapid increase in cyber threats and sophisticated attacks, detecting malicious network activity automatically has become a critical requirement for modern security systems.

This project aims to build a **Machine Learning-based Network Security Threat Detection System** that analyzes network traffic patterns and classifies network connections into:

- ✅ **Normal Traffic** — Legitimate network activity
- 🚨 **Malicious Traffic** — Potentially harmful or suspicious activity

The goal is to develop an automated, scalable, and production-ready ML pipeline capable of identifying security threats efficiently.

## 🚀 Features

### 1. 📥 Data Ingestion

**Responsibilities:**

The Data Ingestion component is responsible for collecting raw network security data and preparing it for the ML pipeline.

- 🔗 Connects with **MongoDB database** to fetch raw phishing/network security data.
- 📂 Extracts and stores raw data into the feature store.
- 🔀 Splits the dataset into **training and testing datasets**.
- 📦 Generates ingestion artifacts required for downstream pipeline components.

**Output Structure:**

```text
Artifacts/
└── data_ingestion/
    ├── feature_store/
    └── ingested/
        ├── train.csv
        └── test.csv

```
### 2. ✅ Data Validation

The **Data Validation** component ensures that the dataset is reliable, consistent, and suitable for machine learning model training.

#### Responsibilities:

- 🔍 Validates incoming data quality before model training
- 📋 Ensures dataset structure matches the expected schema  
- 📊 Detects data distribution changes between training and incoming datasets

---

#### Validation Steps

**1. Schema Validation**

Checks whether the dataset follows the expected structure:
- Number of columns
- Column names
- Data types
- Required features availability

**2. Numerical Column Validation**

Ensures that all required numerical features:
- Exist in the dataset
- Contain valid numerical values
- Match expected data formats

**3. Dataset Drift Detection**

Detects changes in data distribution using the **Kolmogorov-Smirnov (KS) Test**.

The KS test compares the statistical distribution of training data and incoming data to identify significant changes that may impact model performance.

---

#### 📊 Data Validation Flow

![alt text](image-2.png)

---

#### Generated Artifacts

```text
Artifacts/
└── data_validation/
    ├── validated/
    │   ├── train.csv
    │   └── test.csv
    ├── invalid/
    │   ├── train.csv
    │   └── test.csv
    └── drift_report.yaml
