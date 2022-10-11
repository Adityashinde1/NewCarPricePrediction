import os
from from_root import from_root
from car_price.utils.main_utils import MainUtils
from car_price.constant import *


class DataIngestionConfig:
    def __init__(self):
        self.UTILS = MainUtils()
        self.SCHEMA_CONFIG = self.UTILS.read_schema_file_path()
        self.DB_NAME = DB_NAME
        self.COLLECTION_NAME = COLLECTION_NAME
        self.DROP_COLS = list(self.SCHEMA_CONFIG["drop_columns"])
        self.ARTIFCATS_DIR = os.path.join(from_root(), ARTIFACTS_DIR, DATA_INGESTION_ARTIFACTS_DIR)
        self.TRAIN_DATA_ARTIFACT_FILE_DIR = os.path.join(from_root(), ARTIFACTS_DIR, DATA_INGESTION_ARTIFACTS_DIR, DATA_INGESTION_TRAIN_DIR)
        self.TEST_DATA_ARTIFACT_FILE_DIR = os.path.join(from_root(), ARTIFACTS_DIR, DATA_INGESTION_ARTIFACTS_DIR, DATA_INGESTION_TEST_DIR)
        self.TRAIN_DATA_FILE_PATH = os.path.join(from_root(), ARTIFACTS_DIR, DATA_INGESTION_ARTIFACTS_DIR, DATA_INGESTION_TRAIN_DIR, DATA_INGESTION_TRAIN_FILE_NAME)
        self.TEST_DATA_FILE_PATH = os.path.join(from_root(), ARTIFACTS_DIR, DATA_INGESTION_ARTIFACTS_DIR, DATA_INGESTION_TEST_DIR, DATA_INGESTION_TEST_FILE_NAME)

    def get_data_ingestion_config(self):
        return self.__dict__


class DataValidationConfig:
    def __init__(self):
        self.UTILS = MainUtils()
        self.SCHEMA_CONFIG = self.UTILS.read_schema_file_path()
        self.validation_status = False

    def get_data_validation_config(self):
        return self.__dict__


class DataTransformationConfig:
    def __init__(self):
        self.UTILS = MainUtils()        
        self.SCHEMA_CONFIG = self.UTILS.read_schema_file_path()

    def get_data_transformation_config(self):
        return self.__dict__


class ModelTrainerConfig:
    def __init__(self):
        self.UTILS = MainUtils() 

    def get_model_trainer_config(self):
        return self.__dict__


class S3Config:
    def __init__(self):
        self.IO_FILES_BUCKET = CAR_PRICE_INPUT_FILES_BUCKET
        
    def get_s3_config(self):
        return self.__dict__
