import argparse, configparser, time
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from modeling.utils import load_data, get_pipeline, save_model
from modeling.model import Model
from modeling.lemmas import LemmasPt
from modeling.evaluate_model import nested_cross_validation, evaluate_model_performance
from preprocessing.semantic_assembler import get_lemmas_performance
from preprocessing.morphological_assembler import subject_analyzer
from preprocessing.dictionary_assembler import create_dict
from preprocessing.utils import Method, LANGUAGE_DETECT
from preprocessing.assembler import assemble

def evaluate():
    """For each model, hyperparameters tuning with cross-validation. 
    Evaluates the model regarding different algorithms. Trains a new model 
    with the best algorithm and parameters, 
    outputting the performance results into a txt file. 

    """
    filename = './modeling/evaluation/results' + time.strftime("%Y%m%d-%H%M%S") + '.txt'
    results_file = open(filename, 'w')

    label_dataset, features_dataset = load_data()
    pipeline = get_pipeline()
    transformed_features_dataset = pipeline.fit_transform(features_dataset)
    features_train, features_test, labels_train, labels_test = train_test_split(transformed_features_dataset, label_dataset, test_size=0.5, random_state=42, stratify=label_dataset)
    grid_searches, best_estimator_index = nested_cross_validation(features_train, labels_train, results_file)
    
    pipeline.steps.append(['model', grid_searches[best_estimator_index][1]])
    pipeline.fit(features_dataset, label_dataset)
    save_model(pipeline)

    evaluate_model_performance(grid_searches, features_test, labels_test, results_file)

    print("Nested Cross Validation done.") 

def train():
    """Trains a model using Random Forest Classifier.

    """
    label_dataset, features_dataset = load_data()

    pipeline = get_pipeline()
    model = RandomForestClassifier(bootstrap =False, max_depth=25, max_features='sqrt', min_samples_split=10, n_estimators=500)
    
    pipeline.steps.append(['model', model])
    pipeline.fit(features_dataset, label_dataset)
    save_model(pipeline)    
    print("The model is ready.") 

def classify_subject(country: str, sector: str, subject: str, model: Model, pt_lemmas: LemmasPt):
    """Classifies a new subject. 

    Args:
        country: customer country.
        sector: customer business sector.
        subject: subject to be classified.
        model: model.
        pt_lemmas: Portuguese extra lemmas.

    Returns:
        quality: integer from 1 to 5 representing the subject quality.

    """

    features = [country, sector]

    for feature in subject_analyzer(subject):
        features.append(feature)
    
    for feature in get_lemmas_performance(Method.WEIGHTED_AVG, LANGUAGE_DETECT, country, subject, pt_lemmas):
        features.append(feature)  

    features_dataframe = pd.DataFrame([features], columns=['country', 'sector', 'nr_words','nr_chars','case_percentage','punctuation','prefix','emojis','personalization','special_chars','numbers','currency','lemmas_past_performance','nr_lemmas'])
    quality = model.predict(features_dataframe)
    
    print("\nSubject: ", subject)
    print("Features: ", features)
    print("Subject quality: ", quality)
    return quality

def main():
    parser = argparse.ArgumentParser('Train or evaluate a model to predict a subject quality')
    parser.add_argument('method', choices=['train', 'evaluate', 'classify', 'assemble'], type=str, help='Method to be executed: train, evaluate or classify', default="classify")
    parser.add_argument('-c', type=str, help='Country')
    parser.add_argument('-s', type=str, help='Sector')
    parser.add_argument('-subject', type=str, nargs='*', help='Subject to evaluate')

    args = parser.parse_args()
    if args.method != 'classify' and args.c:
        parser.error('country can only be set when --method=classfify.')
    if args.method != 'classify' and args.s:
        parser.error('sector can only be set when --method=classfify.')
    if args.method != 'classify' and args.subject:
        parser.error('subject can only be set when --method=classfify.')

    if args.method == 'train':
        train()
    elif args.method == 'evaluate':
        evaluate()
    elif args.method == 'classify':
        subject = ' '.join(args.subject)
        classify_subject(args.c, args.s, subject, Model.get_instance(), LemmasPt.get_instance())
    elif args.method == 'assemble':
        create_dict()
        assemble()
    else: print('Try another method: train, evaluate or classify. Or try --help')

if __name__ == '__main__':
    main()