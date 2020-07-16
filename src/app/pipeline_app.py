"""This file is the pipeline"""

# import relation package.

# import project package.
from config.config_setting import ConfigSetting
from src.service.data_etl_service import DataEtlService

class PipelineAPP:
    def __init__(self):
        config_setting = ConfigSetting()
        self.config = config_setting.yaml_parser()
        self.log = config_setting.set_logger(["data_etl_app"])
        self.data_etl_service = DataEtlService()
    
    def all_pipeline(self):
        self.etl()
        self.train()
        self.evaluate()
    
    def etl(self):
        pass

    def train(self):
        pass

    def evaluate(self):
        pass