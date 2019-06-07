import time, csv, sys
from .morphological_assembler import subject_analyzer
from .utils import get_rating, Method, ZERO_LEMMAS, NR_LEMMAS, LANGUAGE_DETECT, discard_subject, get_data
from .semantic_assembler import get_lemmas_performance
from .dictionary_assembler import load_pt_lemmas

def assemble():
    """Creates the data file from the recent data available in the dataset and preprocesses the data.
    Transforms the subject into structural and content features. 
    
    """
    table = get_data()
    pt_lemmas = load_pt_lemmas('./preprocessing/pt_lemmas/lemma_pairs.csv')
    filename = './data/data.csv'
    with open(filename, 'w') as incsvfile:
        writer = csv.writer(incsvfile)
        writer.writerow(['quality_class', 'country','sector','nr_words','nr_chars','case_percentage','punctuation','prefix','emojis','personalization','special_chars','numbers', 'currency', 'lemmas_past_performance', 'nr_lemmas'])
        for row in table:
            if not discard_subject(row.subject, row.unique_open_rate, row.country):
               morphological_features = subject_analyzer(row.subject)
               sector = str(row.sector).replace('N/A', 'Undefined') 
               semantic_features = get_lemmas_performance(Method.MAX.value, LANGUAGE_DETECT, row.country, row.subject, pt_lemmas)
               if semantic_features[NR_LEMMAS] != ZERO_LEMMAS: 
                   label = [get_rating(row.unique_open_rate*100)]
                   features = [str(row.country), sector] + morphological_features + semantic_features
                   writer.writerow(label + features)
               else: continue
    print("CSV file updated with success.")