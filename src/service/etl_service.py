"""This file is the pipeline for data etl"""

# import relation package.
import time
from mlflow import log_param

# import project package.
from config.config_setting import ConfigSetting
from src.service.etl.titanic_data_etl_service import TitanicDataEtlService


class EtlService:
    def __init__(self):
        config_setting = ConfigSetting()
        self.config = config_setting.yaml_parser()
        self.log = config_setting.set_logger(["data_etl_service"])
        self.data_etl_service = {}

    def titanic_data_etl(self):
        log_param("dataset", "titanic")
        start_time = time.time()
        self.data_etl_service['titanic'] = TitanicDataEtlService()
        self.log.info('=== Dataset: titanic dataset. ===')
        self.data_etl_service['titanic'].extract_data()
        self.log.info('=== Finish extract the data. ===')
        self.data_etl_service['titanic'].transform_data()
        self.log.info('=== Finish transform the data. ===')
        self.data_etl_service['titanic'].load_to_data()
        self.log.info('=== Finish load the data to file. ===')
        log_param("etl_time", time.time()-start_time)
    
    def other_data_etl(self):
        pass
