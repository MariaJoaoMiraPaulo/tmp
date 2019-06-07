from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, BaggingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import KFold, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, make_scorer, f1_score
from sklearn.neural_network import MLPClassifier
import pandas as pd
import numpy as np

def nested_cross_validation(features: pd.DataFrame, labels: pd.DataFrame, results_file):
    """Hyperparameters tuning with cross validation.

    Args:
        features: data features.
        labels: data labels.
        results_file: File used to output and save the performance results. 

    Returns: 
        grid_search: grid containing the chosen models with tunned parameters.
        best_model_idx: id of the algorithm performing best.

    """
    params = [
        {'n_estimators': [10,100,500], 'max_features': list(range(1, features.shape[1]))},
        {'hidden_layer_sizes': [(50, 50, 50), (50, 100, 50), (100,)], 'learning_rate': ['constant', 'invscaling', 'adaptive']},
        {},
        {'n_estimators': [10,100,500]},
        {'C':[0.1, 100], 'gamma': [0.1, 100]},
        {'criterion': ['gini', 'entropy'], 'max_depth': list(range(1,30)), 'min_samples_leaf': np.linspace(0.1, 10) }]

    outer_score = []
    outer_params = []
    grid_search = []
    models = [("Random Forest", RandomForestClassifier()),("Neural Network", MLPClassifier()), ('Naive Bayes', GaussianNB()), ('AdaBoost', AdaBoostClassifier()),('SVM', SVC()), ("Decision Tree", DecisionTreeClassifier())]
    f1_average = make_scorer(f1_score, average='weighted')

    for idx, entry in enumerate(models):
        (model_name , model) = entry
        param_grid = dict(params[idx])
        grid = GridSearchCV(model, param_grid, cv=10, scoring=f1_average, refit=True, verbose=2, n_jobs=3)
        grid.fit(features, np.ravel(labels))          
        outer_score.append(grid.best_score_)
        outer_params.append(grid.best_params_)
        grid_search.append((model_name, grid.best_estimator_))
        if idx == 0:
            feature_importances = pd.DataFrame(grid.best_estimator_.feature_importances_, index = ['argentina','australia','brasil','chile','colombia','espanha','france','germany','mexico','peru','portugal','united_kingdom','united_states_of_america','Accounting/Financial Services','Architecture/Construction','Arts and Entertainment','Beauty/Health','Church','E-commerce','Education','Food','Government','Hotel,Restaurant and Travel','Information Technologies','Insurance','Manufacturing','Marketing','Non-profit','Other','Publishing/Media','Real Estate','Retail','Services','Undefined','nr_ words','nr_chars','case_percentage','punctuation', 'prefix','emojis','personalization','special_chars','numbers','currency'], columns=['importance']).sort_values('importance', ascending=False)
            print("Feature Importance : ", file=results_file)
            print(feature_importances, file=results_file)

    best_model_idx = outer_score.index(max(outer_score))
    print("Best model: ", best_model_idx, file=results_file)
    print("Best params: ", outer_params[best_model_idx], file=results_file)
    
    return grid_search, best_model_idx

def evaluate_model_performance(models: GridSearchCV, features: pd.DataFrame, labels: pd.DataFrame, results_file):
    """For each tunned model, calculates the overall performance.

    Args:
        models: tunned models.
        features: data features.
        labels: data labels.
        results_file: File used to output and save the performance results. 

    """
    for idx, entry in enumerate(models):
        (model_name , model) = entry
        predicted_labels = model.predict(features)
        print("Model: ", model_name, file=results_file)
        print(classification_report(labels, predicted_labels, target_names = ['1', '2', '3', '4', '5']), file=results_file)
        print(confusion_matrix(labels, predicted_labels), file=results_file)
        print("Accuracy: ", accuracy_score(labels, predicted_labels), file=results_file)

