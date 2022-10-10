import logging
import sys
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from typing import Tuple
from car_price.exception import CarException
from car_price.configuration.mongo_operations import MongoDBOperation
from car_price.entity.config_entity import DataIngestionConfig
from car_price.constant import TEST_SIZE

log_writer = logging.getLogger(__name__)



class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.mongo_op = MongoDBOperation()

    def get_data_from_mongodb(self) -> DataFrame:
        log_writer.info("Entered get_data_from_mongodb method of Data_Ingestion class")
        try:
            log_writer.info("Getting the dataframe from mongodb")
            df = self.mongo_op.get_collection_as_dataframe(
                self.data_ingestion_config.DB_NAME, self.data_ingestion_config.COLLECTION_NAME
            )
            log_writer.info("Got the dataframe from mongodb")
            log_writer.info(
                "Exited the get_data_from_mongodb method of Data_Ingestion class"
            )
            return df

        except Exception as e:
            raise CarException(e, sys) from e


    @staticmethod
    def split_data_as_train_test(df:DataFrame) -> Tuple[DataFrame, DataFrame]:
        log_writer.info(
            "Entered split_data_as_train_test method of Data_Ingestion class"
        )
        try:
            train_set, test_set = train_test_split(df, test_size=TEST_SIZE)
            log_writer.info("Performed train test split on the dataframe")
            log_writer.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )
            return train_set, test_set

        except Exception as e:
            raise CarException(e, sys) from e


    def initiate_data_ingestion(self) -> Tuple[DataFrame, DataFrame]:
        log_writer.info(
            "Entered initiate_data_ingestion method of Data_Ingestion class"
        )
        try:
            df = self.get_data_from_mongodb()
            df1 = df.drop(self.data_ingestion_config.DROP_COLS, axis=1)
            log_writer.info("Got the data from mongodb")
            train_set, test_set = self.split_data_as_train_test(df1)
            log_writer.info("Performed train test split on the dataset")
            log_writer.info(
                "Exited initiate_data_ingestion method of Data_Ingestion class"
            )
            return train_set, test_set

        except Exception as e:
            raise CarException(e, sys) from e
