from os import environ


CONFIG_FILE_PATH = "config/config.yaml"
SCHEMA_FILE_PATH = "config/schema.yaml"

DB_NAME = 'ineuron'
COLLECTION_NAME = 'car'
DB_URL = environ["MONGODB_URL"]

TEST_SIZE = 0.2

MODEL_CONFIG_FILE = 'config/model.yaml'

ARTIFACTS_DIR = 'artifacts'
LOGS_DIR = 'logs'
LOGS_FILE_NAME = 'car_price.log'

PREPROCESSOR_OBJECT_FILE_NAME = ARTIFACTS_DIR + "/" + "car_price_preprocessor.pkl"

CAR_PRICE_INPUT_FILES_BUCKET = 'car-price-io-files'

MODEL_FILE_NAME = 'model'
MODEL_SAVE_FORMAT = '.sav'
BEST_MODEL_PATH = ARTIFACTS_DIR + "/" + MODEL_FILE_NAME + MODEL_SAVE_FORMAT

APP_HOST = '0.0.0.0'
APP_PORT = 8080