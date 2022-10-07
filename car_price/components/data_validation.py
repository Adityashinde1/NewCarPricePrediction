import json
import logging
import sys
from pandas import DataFrame
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from typing import Tuple, Union
from car_price.exception import CarException
from car_price.entity.config_entity import DataValidationConfig

log_writer = logging.getLogger(__name__)


class DataValidation:
    def __init__(self, train_set, test_set):

        self.data_validation_config = DataValidationConfig()

        self.train_set = train_set

        self.test_set = test_set

    def validate_schema_columns(self, df: DataFrame) -> bool:
        try:
            if len(df.columns) == len(self.data_validation_config.SCHEMA_CONFIG['columns']):                       
                validation_status = True

            else:
                validation_status = False

            return validation_status

        except Exception as e:
            raise CarException(e, sys) from e

    def validate_schema_for_numerical_datatype(self, df: DataFrame) -> bool:
        try:
            for column in self.data_validation_config.SCHEMA_CONFIG["numerical_columns"]:

                if column in df.columns:
                    validation_status = True

                else:
                    validation_status = False

            return validation_status

        except Exception as e:
            raise CarException(e, sys) from e        

    def validate_schema_for_categorical_datatype(self, df: DataFrame) -> bool:
        try:
            for column in self.data_validation_config.SCHEMA_CONFIG["categorical_columns"]:
             
                if column in df.columns:
                    validation_status = True

                else:
                    validation_status = False

            return validation_status

        except Exception as e:
            raise CarException(e, sys) from e   

    def validate_dataset_schema_columns(self) -> Tuple[bool, bool]:
        logging.info(
            "Entered validate_dataset_schema_columns method of Data_Validation class"
        )

        try:
            logging.info("Validating dataset schema columns")

            train_schema_status = self.validate_schema_columns(self.train_set)

            logging.info("Validated dataset schema columns on the train set")

            test_schema_status = self.validate_schema_columns(self.test_set)

            logging.info("Validated dataset schema columns on the test set")

            logging.info("Validated dataset schema columns")

            return train_schema_status, test_schema_status

        except Exception as e:
            raise CarException(e, sys) from e

    def validate_dataset_schema_for_numerical_datatype(self) -> Tuple[bool, bool]:
        logging.info(
            "Entered validate_dataset_schema_for_numerical_datatype method of Data_Validation class"
        )

        try:
            logging.info("Validating dataset schema for numerical datatype")

            train_num_datatype_status = self.validate_schema_for_numerical_datatype(
                self.train_set
            )

            logging.info(
                "Validated dataset schema for numerical datatype for train set"
            )

            test_num_datatype_status = self.validate_schema_for_numerical_datatype(
                self.test_set
            )

            logging.info("Validated dataset schema for numerical datatype for test set")

            logging.info(
                "Exited validate_dataset_schema_for_numerical_datatype method of Data_Validation class"
            )

            return train_num_datatype_status, test_num_datatype_status

        except Exception as e:
            raise CarException(e, sys) from e

    def validate_dataset_schema_for_categorical_datatype(self) -> Tuple[bool, bool]:
        logging.info(
            "Entered validate_dataset_schema_for_numerical_datatype method of Data_Validation class"
        )

        try:
            logging.info("Validating dataset schema for numerical datatype")

            train_cat_datatype_status = self.validate_schema_for_categorical_datatype(
                self.train_set
            )

            logging.info(
                "Validated dataset schema for numerical datatype for train set"
            )

            test_cat_datatype_status = self.validate_schema_for_categorical_datatype(
                self.test_set
            )

            logging.info("Validated dataset schema for numerical datatype for test set")

            logging.info(
                "Exited validate_dataset_schema_for_numerical_datatype method of Data_Validation class"
            )

            return train_cat_datatype_status, test_cat_datatype_status

        except Exception as e:
            raise CarException(e, sys) from e

    def detect_dataset_drift(self, reference: DataFrame, production: DataFrame, get_ratio: bool = False) -> Union[bool, float]:
        try:
            data_drift_profile = Profile(sections=[DataDriftProfileSection()])

            data_drift_profile.calculate(reference, production)

            report = data_drift_profile.json()

            json_report = json.loads(report)

            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]

            n_drifted_features = json_report["data_drift"]["data"]["metrics"][
                "n_drifted_features"
            ]

            if get_ratio:
                return n_drifted_features / n_features

            else:
                return json_report["data_drift"]["data"]["metrics"]["dataset_drift"]

        except Exception as e:
            raise CarException(e, sys) from e

    def initiate_data_validation(self) -> bool:
        log_writer.info("Entered initiate_data_validation method of Data_Validation class")

        try:
            log_writer.info("Initiated data validation for the dataset")

            drift = self.detect_dataset_drift(self.train_set, self.test_set)

         
            (
                schema_train_col_status,
                schema_test_col_status,
            ) = self.validate_dataset_schema_columns()

            log_writer.info(
                f"Schema train cols status is {schema_train_col_status} and schema test cols status is {schema_test_col_status}"
            )

            log_writer.info("Validated dataset schema columns")

            (
                schema_train_cat_cols_status,
                schema_test_cat_cols_status,
            ) = self.validate_dataset_schema_for_categorical_datatype()

            log_writer.info(
                f"Schema train cat cols status is {schema_train_cat_cols_status} and schema test cat cols status is {schema_test_cat_cols_status}"
            )

            log_writer.info("Validated dataset schema for catergorical datatype")

            (
                schema_train_num_cols_status,
                schema_test_num_cols_status,
            ) = self.validate_dataset_schema_for_numerical_datatype()

            log_writer.info(
                f"Schema train numerical cols status is {schema_train_num_cols_status} and schema test numerical cols status is {schema_test_num_cols_status}"
            )

            log_writer.info("Validated dataset schema for numerical datatype")

            if (
                schema_train_cat_cols_status is True
                and schema_test_cat_cols_status is True
                and schema_train_num_cols_status is True
                and schema_test_num_cols_status is True
                and schema_train_col_status is True
                and schema_test_col_status is True
            ):
                log_writer.info("Dataset schema validation completed")

                return True

            else:
                return False

        except Exception as e:
            raise CarException(e, sys) from e
