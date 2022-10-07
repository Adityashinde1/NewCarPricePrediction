import logging
import sys
from typing import List, Tuple
from pandas import DataFrame
from car_price.entity.config_entity import ModelTrainerConfig
from car_price.entity.tuner_config import *
from car_price.exception import CarException
from car_price.constant import PREPROCESSOR_OBJECT_FILE_NAME, BEST_MODEL_PATH



class CarPriceModel:
    def __init__(self, preprocessing_object: object, trained_model_object: object):
        self.preprocessing_object = preprocessing_object

        self.trained_model_object = trained_model_object

    def predict(self, X) -> DataFrame:
        logging.info("Entered predict method of CarPriceModel class")

        try:
            logging.info("Using the trained model to get predictions")

            transformed_feature = self.preprocessing_object.transform(X)

            logging.info("Used the trained model to get predictions")

            return self.trained_model_object.predict(transformed_feature)

        except Exception as e:
            raise CarException(e, sys) from e

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

        self.model_tuner_config = TunerConfig()

    def get_trained_models(self, X_data: DataFrame, Y_data: DataFrame) -> List[Tuple[float, object, str]]:

        logging.info("Entered get_trained_models method of ModelTrainer class")

        try:
            model_config = self.model_trainer_config.UTILS.read_model_config_file()

            models_list = list(model_config["train_model"].keys())

            logging.info("Got model list from the config file")

            x_train, y_train, x_test, y_test = (
                X_data[:, :-1],
                X_data[:, -1],
                Y_data[:, :-1],
                Y_data[:, -1],
            )

            tuned_model_list = [
                (
                    self.model_trainer_config.UTILS.get_tuned_model(
                        model_name, x_train, y_train, x_test, y_test,
                    )
                )
                for model_name in models_list
            ]

            logging.info("Got trained model list")

            logging.info("Exited the get_trained_models method of ModelFinder class")

            return tuned_model_list

        except Exception as e:
            raise CarException(e, sys) from e

    def initiate_model_trainer(self, train_set, test_set) -> None:

        logging.info(
            "Entered initiate_model_trainer nethod of ModelTrainer class"
        )

        try:
            list_of_trained_models = self.get_trained_models(train_set, test_set)

            logging.info(
                "Got a list of tuple of model score,model and model name"
            )

            (
                best_model,
                best_model_score,
            ) = self.model_trainer_config.UTILS.get_best_model_with_name_and_score(list_of_trained_models)

            logging.info("Got best model score,model and model name")

            preprocessing_obj = self.model_trainer_config.UTILS.load_object(PREPROCESSOR_OBJECT_FILE_NAME)

            model_config = self.model_trainer_config.UTILS.read_model_config_file()

            logging.info("Loaded preprocessing object")

            base_model_score = float(model_config['base_model_score'])

            if best_model_score >= base_model_score:
                self.model_trainer_config.UTILS.update_model_score(best_model_score)

                logging.info("Updating model score in yaml file")

                carprice_model = CarPriceModel(preprocessing_obj, best_model)

                logging.info(
                    "Created car price model object with preprocessor and model"
                )

                logging.info("Created best model file path")

                self.model_trainer_config.UTILS.save_object(BEST_MODEL_PATH, carprice_model)

                logging.info("Saved the best model object path")

            else:
                logging.info("No best model found with score more than base score")

                raise "No best model found with score more than base score "

        except Exception as e:
            raise CarException(e, sys) from e


