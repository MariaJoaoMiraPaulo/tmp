import pickle, time
import pandas as pd
import numpy as np
import os
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin

def save_model(pipeline: Pipeline):
    """Saves pipeline in trained models directory. 

    Args: 
        pipeline: the model to be saved.
        
    """
    new_filename = './modeling/trained_models/pipeline' + time.strftime("%Y%m%d-%H%M%S") + '.p'
    filename = './modeling/trained_models/pipeline.p'
    os.rename(filename, new_filename)
    pickle.dump(pipeline, open(filename, 'wb'))
    
    print("Trained Model and saved pipeline.")

def load_model():
    """Loads and returns the most recent model.

    Returns:
        pipeline: trained model 

    """
    with open('./modeling/trained_models/pipeline.p', 'rb') as pipeline_file:
        pipeline = pickle.load(pipeline_file)
        return pipeline
  
def load_data():
    """Returns features and respective labels.

    Returns:
        label_dataset: DataFrame containing labels.
        features_dataset: DataFrame containing features.

    """
    label_dataset = pd.read_csv('./data/data_WAVG.csv', usecols=[0])
    features_dataset = pd.read_csv('./data/data_WAVG.csv', usecols=['country','sector','nr_words','nr_chars','case_percentage','punctuation','prefix','emojis','personalization','special_chars','numbers','currency', 'lemmas_past_performance', 'nr_lemmas'])

    return label_dataset, features_dataset
    
def load_pt_lemmas(path_to_lemmas: str):
    """Returns portuguese extra lemmas.

    Args: 
        path_to_lemmas: Relaive path to pt_lemmas file. 

    Returns:
        dict: dictionary containing Portuguese words and respective lemmas.

    """
    pt_lemmas_list = pd.read_csv(path_to_lemmas)
    return {row[1]: row[0] for row in pt_lemmas_list.values}

def get_pipeline():
    """Returns pipeline with data preprocessing steps.

     Returns:
        pipeline: pipeline.

    """
    categorical_transformer = Pipeline(steps=[('hotencoder', OneHotEncoder(handle_unknown='ignore', sparse=False))])
    numerical_transformer = Pipeline(steps=[('minmax', MinMaxScaler(feature_range=(0, 1), copy=False))])
    transformer =ColumnTransformer(transformers=[('categorical', categorical_transformer, ['country', 'sector']), ('numerical', numerical_transformer, ['nr_words', 'nr_chars', 'case_percentage'])], remainder='passthrough')

    data_pipeline = Pipeline(steps=[
         ('dropcolumns', ColumnDropper(col=['lemmas_past_performance', 'nr_lemmas'])),
         ('preprocessing', transformer)])

    return data_pipeline

class ColumnDropper(BaseEstimator, TransformerMixin):

    def __init__( self, col ):
        self.col = col 

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        return X.drop(columns = self.col)