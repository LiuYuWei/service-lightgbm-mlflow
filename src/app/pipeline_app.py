"""This file is the pipeline"""

# import relation package.

# import project package.
from config.config_setting import ConfigSetting
from src.service.etl_service import EtlService

class PipelineAPP:
    def __init__(self):
        config_setting = ConfigSetting()
        self.config = config_setting.yaml_parser()
        self.log = config_setting.set_logger(["data_etl_app"])
        self.etl_service = EtlService()
    
    def all_pipeline(self):
        self.etl()
        self.train()
        self.evaluate()
    
    def etl(self):
        if self.config['etl']['dataset'] == 'titanic':
            self.etl_service.titanic_data_etl()

    def train(self):
        pass

    def evaluate(self):
        pass