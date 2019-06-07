import argparse, numpy, time
import pandas as pd
from .utils import Method as performance_method
from .dictionary_assembler import load_pt_lemmas, subject_lemmas_analyzer, create_dict
from .dictionary import Dictionary

def main():
    parser = argparse.ArgumentParser('Classify a subject regarding the semantic.')
    parser.add_argument("country", type=str, help="Country")
    parser.add_argument("subject", type=str, nargs='*', help="Subject")
    args = parser.parse_args()
    pt_lemmas = load_pt_lemmas('./preprocessing/pt_lemmas/lemma_pairs.csv')
    print("Lemmas performance: ", get_lemmas_performance(args.country, ' '.join(args.subject), pt_lemmas))

def get_lemmas_performance(method: performance_method, language_detect: bool, country: str, subject: str, pt_lemmas: dict):
    """Returns the feature lemmas_past_performance value, which calculation depends on the employed method.

    Args:
        method: calculation method to be applied.
        language_detect: true if the subject idiom should be identified by the python library detectLang or just by the country.
        country: customer country.
        subject: subject to be analyzed.
        pt_lemmas: dictionary containing extra portuguese lemmas.

    Returns:
        list: list with lemmas_past_performance value and number of lemmas detected.

    """
    dictionary = Dictionary.get_instance()
    lemmas = subject_lemmas_analyzer(language_detect, country, subject, pt_lemmas)
    if method is performance_method.AVG.value:
        return [average(dictionary, lemmas), len(lemmas)]
    elif method is performance_method.WEIGHTED_AVG.value:
        return [weighted_average(dictionary, lemmas), len(lemmas)]
    elif method is performance_method.MAX.value:
        return [max_value_quality(dictionary, lemmas), len(lemmas)]
    else: 
        return [weighted_average(dictionary, lemmas), len(lemmas)]

def weighted_average(dictionary: dict, lemmas: list):
    """Calculates lemmas_past_performance using the weighted average.

    Args:
        dictionary: the dictionary of lemmas to consult.
        lemmas: lemmas to analyze.

    Returns: 
        lemmas_past_performance value.

    """
    data, weights = get_lemmas_info(dictionary, lemmas)    
    return 0 if len(data) == 0 else numpy.average(data, weights = weights)

def average(dictionary: dict, lemmas: list):
    """Calculates lemmas_past_performance using the average.

    Args:
        dictionary: the dictionary of lemmas to consult.
        lemmas: lemmas to analyze.

    Returns: 
        lemmas_past_performance value.

    """
    data, weights = get_lemmas_info(dictionary, lemmas)    
    return 0 if len(data) == 0 else numpy.average(data)

def max_value_quality(dictionary: dict, lemmas: list):
    """Calculates lemmas_past_performance using the max value approach.

    Args:
        dictionary: the dictionary of lemmas to consult.
        lemmas: lemmas to analyze.

    Returns: 
        lemmas_past_performance value.

    """
    data, weights = get_lemmas_info(dictionary, lemmas)    
    return 0 if len(data) == 0 else max(data)

def get_lemmas_info(dictionary: dict, lemmas: list):
    """Finds lemmas information in dictionary.

    Args:
        lemmas: list of lemmas to be analyzed.
        dictionary: dictionary to consult.

    Returns:
        data: list of qualities.
        weights: list of appearances.

    """
    data = []
    weights = []

    for lemma in lemmas:
        dict_value = dictionary.get(lemma)
        if not dict_value == None:
            data.append(dict_value[1])
            weights.append(dict_value[0])

    return data, weights 

if __name__ == '__main__':
    main()