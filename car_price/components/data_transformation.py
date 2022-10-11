import logging
import sys
from pandas import DataFrame
from typing import Union
import numpy as np
from category_encoders.binary import BinaryEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from car_price.entity.config_entity import DataTransformationConfig
from car_price.exception import CarException
from car_price.constant import PREPROCESSOR_OBJECT_FILE_NAME

logger = logging.getLogger(__name__)


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()


    def get_data_transformer_object(self) -> object:
        logger.info(
            "Entered get_data_transformer_object method of Data_Ingestion class"
        )
        try:
            numerical_columns = self.data_transformation_config.SCHEMA_CONFIG["numerical_columns"]
            onehot_columns = self.data_transformation_config.SCHEMA_CONFIG["onehot_columns"]
            binary_columns = self.data_transformation_config.SCHEMA_CONFIG["binary_columns"]
            logger.info(
                "Got numerical cols,one hot cols,binary cols from schema config"
            )
            numeric_transformer = StandardScaler()
            oh_transformer = OneHotEncoder(handle_unknown='ignore')
            binary_transformer = BinaryEncoder()
            logger.info("Initialized StandardScaler,OneHotEncoder,BinaryEncoder")
            preprocessor = ColumnTransformer(
                [
                    ("OneHotEncoder", oh_transformer, onehot_columns),
                    ("BinaryEncoder", binary_transformer, binary_columns),
                    ("StandardScaler", numeric_transformer, numerical_columns),
                ]
            )
            logger.info("Created preprocessor object from ColumnTransformer")
            logger.info(
                "Exited get_data_transformer_object method of Data_Ingestion class"
            )
            return preprocessor

        except Exception as e:
            raise CarException(e, sys) from e


    @staticmethod
    def _outlier_capping(col, df: DataFrame) -> DataFrame:
        logger.info("Entered _outlier_capping method of Data_Transformation class")
        try:
            logger.info("Performing _outlier_capping for columns in the dataframe")
            percentile25 = df[col].quantile(0.25)
            percentile75 = df[col].quantile(0.75)
            iqr = percentile75 - percentile25
            upper_limit = percentile75 + 1.5 * iqr
            lower_limit = percentile25 - 1.5 * iqr
            df.loc[(df[col] > upper_limit), col] = upper_limit
            df.loc[(df[col] < lower_limit), col] = lower_limit
            logger.info(
                "Performed _outlier_capping method of Data_Transformation class"
            )
            logger.info("Exited _outlier_capping method of Data_Transformation class")
            return df

        except Exception as e:
            raise CarException(e, sys) from e


    def initiate_data_transformation(self, train_set: DataFrame, test_set: DataFrame) -> Union[np.ndarray, np.ndarray]:
        logger.info(
            "Entered initiate_data_transformation method of Data_Transformation class"
        )
        try:
            preprocessor = self.get_data_transformer_object()
            logger.info("Got the preprocessor object")
            target_column_name = self.data_transformation_config.SCHEMA_CONFIG["target_column"]
            numerical_columns = self.data_transformation_config.SCHEMA_CONFIG["numerical_columns"]
            logger.info(
                "Got target column name and numerical columns from schema config"
            )
            continuous_columns = [
                feature
                for feature in numerical_columns
                if len(train_set[feature].unique()) >= 25
            ]
            logger.info("Got a list of continuous_columns")
            [self._outlier_capping(col, train_set) for col in continuous_columns]
            logger.info("Outlier capped in train df")
            [self._outlier_capping(col, test_set) for col in continuous_columns]
            logger.info("Outlier capped in test df")
            input_feature_train_df = train_set.drop(
                columns=[target_column_name], axis=1
            )
            target_feature_train_df = train_set[target_column_name]
            logger.info("Got train features and test features")
            input_feature_test_df = test_set.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_set[target_column_name]
            logger.info("Got test features and test features")
            logger.info(
                "Applying preprocessing object on training dataframe and testing dataframe"
            )
            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
            logger.info(
                "Used the preprocessor object to fit transform the train features"
            )
            input_feature_test_arr = preprocessor.transform(input_feature_test_df)
            logger.info("Used the preprocessor object to transform the test features")
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            logger.info("Created train array and test array")
            self.data_transformation_config.UTILS.save_object(PREPROCESSOR_OBJECT_FILE_NAME, preprocessor)
            logger.info("Saved the preprocessor object")
            logger.info(
                "Exited initiate_data_transformation method of Data_Transformation class"
            )
            return train_arr, test_arr

        except Exception as e:
            raise CarException(e, sys) from e
