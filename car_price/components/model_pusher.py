import sys
import os
from car_price.configuration.s3_operations import S3Operation
from car_price.constant import PREPROCESSOR_OBJECT_FILE_NAME
from car_price.entity.config_entity import S3Config
from car_price.entity.config_entity import ModelPusherConfig
from car_price.exception import CarException
import logging


class ModelPusher:
    def __init__(self, model_pusher_config: ModelPusherConfig, 
                    s3: S3Operation, s3_config: S3Config):
        self.model_pusher_config = model_pusher_config
        self.s3 = s3
        self.s3_config = s3_config


    def initiate_model_pusher(self) -> None:
        logging.info("Entered initiate_model_pusher method of ModelTrainer class")
        try:
            logging.info("Uploading artifacts folder to s3 bucket")
            
            self.s3.upload_file(
                self.model_pusher_config.BEST_MODEL_PATH,
                self.model_pusher_config.BEST_MODEL_PATH,
                self.s3_config.IO_FILES_BUCKET,
                remove=False,
            )
            self.s3.upload_file(
                PREPROCESSOR_OBJECT_FILE_NAME,
                PREPROCESSOR_OBJECT_FILE_NAME,
                self.s3_config.IO_FILES_BUCKET,
                remove=False,
            )
            logging.info("Uploaded artifacts folder to s3 bucket")
            logging.info("Exited initiate_model_pusher method of ModelTrainer class")

        except Exception as e:
            raise CarException(e, sys) from e