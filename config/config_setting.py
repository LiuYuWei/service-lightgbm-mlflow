"""This file is used in setting config."""

# import relation package.
import os
import sys
import logging
import logging.config
from datetime import datetime
import yaml

# import project package.
from config.path_setting import PathSetting


class ConfigSetting:
    """This class is used in setting config."""

    def __init__(self):
        """Initial some variable and module"""
        self.path_setting = PathSetting()

    def set_logger(self, name,
                   logger_path_enabled=False,
                   log_dir=os.path.join("tmp", "logs"),
                   logger_config_path='config/yaml/logger_config.yml'):
        """
        set_logger: parser the yaml file.

        Arguments:
        name: The project name of log.
        log_dir: The path of log storage.

        Returns:
        logger: The logger setting variable.
        """
        logger_config_path = self.path_setting.path_join(logger_config_path)

        if os.path.exists(logger_config_path) and (logger_path_enabled):
            with open(logger_config_path, 'r') as f:
                yaml_config = yaml.safe_load(f.read())

            log_dir = self.path_setting.path_join(log_dir)
            self.path_setting.make_directory(log_dir)
            yaml_config["handlers"]["file"]["filename"] = self.path_setting.path_join(
                log_dir, 'project.log'+'.'+datetime.strftime(datetime.now(), '%Y%m%d'))

            logging.config.dictConfig(yaml_config)
            logging.getLogger(name)
        else:
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s][%(module)s][%(funcName)s]%(message)s',
                                datefmt='%a, %d %b %Y %H:%M:%S', stream=sys.stdout)

        return logging

    def yaml_parser(self, project_config_path='config/yaml/project_config.yml'):
        """
        yaml_parser: parser the yaml file.
        Returns:
            data: yaml parameter(See the project_config.yml file.)
        """
        project_config_path = self.path_setting.path_join(project_config_path)
        data = ''
        try:
            with open(project_config_path, 'r', encoding='utf-8') as stream:
                data = yaml.load(stream, Loader=yaml.Loader)
        except IOError as e:
            self.set_logger("[config_setting]").error(e)
        return data
    
    def parameter_parser(self, project_config_path='config/yaml/parameter_config.yml'):
        """
        parameter_parser: parser the parameter file.
        Returns:
            data: parameter parameter(See the parameter_config.yml file.)
        """
        project_config_path = self.path_setting.path_join(project_config_path)
        data = ''
        try:
            with open(project_config_path, 'r', encoding='utf-8') as stream:
                data = yaml.load(stream, Loader=yaml.Loader)
        except IOError as e:
            self.set_logger("[config_setting]").error(e)
        return data
