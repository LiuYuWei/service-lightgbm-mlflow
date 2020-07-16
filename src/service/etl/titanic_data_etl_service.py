"""This file is the pipeline for data etl"""

# import relation package.
import pickle
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from mlflow import log_metric, log_param, log_artifact


# import project package.
from config.config_setting import ConfigSetting


class TitanicDataEtlService:
    def __init__(self):
        config_setting = ConfigSetting()
        self.config = config_setting.yaml_parser()
        self.log = config_setting.set_logger(["data_etl_service"])
        self.df = {}
        self.train_label = []
        self.one_hot_encoder = None
        self.label_encoder = LabelEncoder()
        
    def extract_data(self):
        # read train data
        self.df['train'] = pd.read_csv(self.config['titanic']['extract']['train_file'])
        self.train_label = list(self.df['train'][self.config['titanic']['extract']['train_label']])
        # read test data
        self.df['test'] = pd.read_csv(self.config['titanic']['extract']['test_file'])
        self.log.info("Finish load training data and testing data")
        self.log.info("Length of training data: {}".format(len(self.df['train'])))
        self.log.info("Length of testing data: {}".format(len(self.df['test'])))
        log_param("num_train", len(self.df['train']))
        log_param("num_test", len(self.df['test']))
        
    
    def transform_data(self):
        self.title_generator()
        self.sex_generator()
        self.age_generator()
        self.embark_generator()
        self.cabin_generator()
        self.fare_generator()
        self.remove_feature()
        self.fill_na_value()
    
    def load_to_data(self):
        self.save_dataframe()
        self.save_label()

    def remove_feature(self):
        for table in self.df.values():
            for column in self.config['titanic']['transform']['drop_columns']:
                if column in list(table.columns):
                    table.drop(column,axis=1, inplace=True)
                    self.log.info('Remove columns: {}'.format(column))

    def feature_selection(self):
        total_missing = self.df['train'].isnull().sum()
        to_delete = total_missing[total_missing >
                                  (self.df['train'].shape[0]/3.)]
        for table in self.df.values():
            table.drop(list(to_delete.index), axis=1, inplace=True)

        numerical_features = self.df['test'].select_dtypes(
            include=["float", "int", "bool"]).columns.values
        categorical_features = self.df['train'].select_dtypes(
            include=["object"]).columns.values
        self.log.info("Finish select data feature.")
        self.log.info('Delete feature: {}'.format(list(to_delete.index)))
        self.log.info('numerical_features: {}'.format(list(numerical_features)))
        self.log.info('categorical_features: {}'.format(list(categorical_features)))
        log_param('delete_feature', str(list(to_delete.index)))
        log_param('numerical_features', str(list(numerical_features)))
        log_param('categorical_features', str(list(categorical_features)))
        return numerical_features, categorical_features
    
    def fill_na_value(self):
        for table in self.df.values():
            for col in table.columns:
                table[col].fillna(table.groupby("Title")[col].transform("median"), inplace= True)
        self.log.info("Finish fill na value.")

    def title_generator(self):
        title_mapping = {"Mr": 0, "Miss": 1, "Mrs": 2, 
                        "Master": 3, "Dr": 3, "Rev": 3, "Col": 3, "Major": 3, "Mlle": 3,"Countess": 3,
                        "Ms": 3, "Lady": 3, "Jonkheer": 3, "Don": 3, "Dona" : 3, "Mme": 3,"Capt": 3,"Sir": 3 }
        for table in self.df.values():
            table['Title'] = table['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
            table['Title'] = table["Title"].map(title_mapping)
    
    def sex_generator(self):
        sex_mapping = {"male": 0, "female": 1}
        for table in self.df.values():
            table['Sex'] = table['Sex'].map(sex_mapping)

    def age_generator(self):
        for table in self.df.values():
            table.loc[ table['Age'] <= 16, 'Age'] = 0,
            table.loc[(table['Age'] > 16) & (table['Age'] <= 26), 'Age'] = 1,
            table.loc[(table['Age'] > 26) & (table['Age'] <= 36), 'Age'] = 2,
            table.loc[(table['Age'] > 36) & (table['Age'] <= 62), 'Age'] = 3,
            table.loc[ table['Age'] > 62, 'Age'] = 4
    
    def embark_generator(self):
        embarked_mapping = {'S':0,'C':1,'Q':2}
        for table in self.df.values():
            table['Embarked'] = table['Embarked'].map(embarked_mapping)
    
    def cabin_generator(self):
        cabin_mapping = {"A": 0, "B": 0.4, "C": 0.8, "D": 1.2, "E": 1.6, "F": 2, "G": 2.4, "T": 2.8}
        for table in self.df.values():
            table['Cabin'] = table['Cabin'].map(cabin_mapping)
            table["Cabin"].fillna(table.groupby("Pclass")["Cabin"].transform("median"), inplace=True)
    
    def fare_generator(self):
        for table in self.df.values():
            table.loc[table['Fare'] <= 17, 'Fare'] = 0,
            table.loc[(table['Fare'] > 17) & (table['Fare'] <= 30), 'Fare'] = 1,
            table.loc[(table['Fare'] > 30) & (table['Fare'] <= 100), 'Fare'] = 2,
            table.loc[table['Fare'] >= 100, 'Fare'] = 3

    def save_dataframe(self, save_file_path=None):
        if save_file_path is None:
            save_file_path = self.config['titanic']['load_to']['save_file_path']
        self.df['train'].to_csv("{}/{}".format(save_file_path, 'train.csv'), index=False)
        self.df['test'].to_csv("{}/{}".format(save_file_path, 'test.csv'), index=False)
        log_artifact("{}/{}".format(save_file_path, 'train.csv'))
        log_artifact("{}/{}".format(save_file_path, 'test.csv'))
        self.log.info('Successfully save the dataframe file.')
    
    def save_label(self, save_file_path=None):
        if save_file_path is None:
            save_file_path = self.config['titanic']['load_to']['save_file_path']
        file_path = "{}/{}".format(save_file_path, 'training_label.pkl')
        file = open(file_path, 'wb')
        pickle.dump(self.train_label, file)
        file.close()
        log_artifact(file_path)
        self.log.info('Successfully save the label.')
