from langdetect import detect
import pandas as pd
import spacy, csv, numpy, time, sys, unidecode, re
sys.path.append("..")
import preprocessing.utils as utils
pt_parser = spacy.load('pt')
es_parser = spacy.load('es')
en_parser = spacy.load('en')

dictionary = {}

def detect_language(country: str, subject: str):
    """Detects the subject language. If it is impossible to detect, returns the country idiom.

    Returns:
        str: language code.

    """
    try:
        language = detect(subject)
        return language
    except:
        return get_country_language(country)

def get_country_language(country: str):
    """Retuns the country oficial language code.

    Returns:
        str: language code.
        
    """
    if country == 'portugal' or country == 'brasil' or country == 'mozambique' or country == 'angola':
        return 'pt'
    elif country == 'chile' or country == 'argentina' or country=='honduras' or country == 'colombia' or country == 'espanha' or country == 'peru' or country == 'mexico':
        return 'es'
    elif country =='malta' or country == 'australia' or country=='curacao' or country == 'united_states_of_america' or country == 'united_kingdom':
        return 'en'
    return 'not recognized'

def parse_subject(language: str, subject: str, pt_lemmas: dict):
    """Finds out the lemmas contained in the subject. 

    Args: 
        language: language code.
        subject: subject to be lemmatized.
        pt_lemmas: dict containing extra portuguese lemmas.

    Returns:
        list: list of lemmas.

    """
    words = []
    if language == 'pt':
        tokens = pt_parser(subject)
    elif language == 'en':
        tokens = en_parser(subject)
    elif language == 'es':
        tokens = es_parser(subject)
    else: 
        return []

    for token in tokens:
        if not token.is_stop and len(token.text) >= 4 and len(token.text) < 16:
            if language == 'pt':
                lemma = pt_lemmas.get(token.text, token.lemma_)
                words.append(lemma)
            else: words.append(token.lemma_)

    return words

def clean_subject(subject: str):
    """Cleans a subject.

    Args:
        subject: subject to be cleaned.

    Returns:
        string: lowercase subject without any special chars, emojis, personalization codes or numbers. 
    
    """
    subject = subject.lower()
    personalization_codes = ['!fname', '!fullname', '!email', '!lname', '!birth_date', '!extra_field_1101', '!telephone', '!cellphone']
    for code in personalization_codes:
        subject = subject.replace(code,"")
    subject = re.sub(r'[^a-záàãéêíóõúç]', ' ', subject)

    return ' '.join(subject.split())

def subject_lemmas_analyzer(language_detect: bool, country: str, subject: str, pt_lemmas: dict):
    """Sums up the content analysis: cleans subject, detects language and finds out the existent lemmas.

    Args:
        language_detect: true if the subject idiom should be identified by the python library detectLang or just by the country.
        country: customer country.
        subject: subject to be analyzed.
        pt_lemmas: dictionary containing extra portuguese lemmas.


    """
    cleaned_subject = clean_subject(subject)
    if language_detect:
        language = detect_language(country,cleaned_subject)
    else: language = get_country_language(country)
    return parse_subject(language, cleaned_subject, pt_lemmas)

def update_dict(word: str, open_rate: float):
    """Updates the lemma quality on dictionary of lemmas.  

    Args:
        word: lemma to be updated.
        open_rate: lemma quality, expressed by the open rate.
    
    """
    if word in dictionary:
        dictionary[word][0] += 1
        dictionary[word][1] = (float(dictionary[word][1]) + open_rate)
    else: dictionary[word] = [1,open_rate]

def write_to_dict(dictionary: dict):
    """Creates dictionary file.

    Args:
        dict: dictionary containing lemmas and respective average quality.
    
    """
    filename = './data/dictionary.csv'
    with open(filename, 'w') as incsvfile:
        writer = csv.writer(incsvfile)
        writer.writerow(['word', 'count', 'avg_rate'])
        for key, value in sorted(dictionary.items()):
            dict_row = [key, str(value[0]), utils.get_rating(value[1]/value[0])]
            writer.writerow(dict_row)
        
def load_pt_lemmas(path_to_lemmas: str):
    """Loads portuguese lemmas dictionary.

    Args:
        path_to_lemmas: Relaive path to pt_lemmas file. 

    Returns:
        dict: dicitionary with all lemmas and respective average quality.
    
    """
    pt_lemmas_list = pd.read_csv(path_to_lemmas)
    return {row[1]: row[0] for row in pt_lemmas_list.values}

def create_dict():
    """Creates dictionary, looping through all the existent subjects in the dataset.
    
    """
    pt_lemas = load_pt_lemmas('./preprocessing/pt_lemmas/lemma_pairs.csv')
    table = pd.DataFrame(list(utils.get_data()))
    for index, row in table.iterrows():
        if not utils.discard_subject(row['subject'], row['unique_open_rate'], row['country']):
            lemmas = subject_lemmas_analyzer(utils.LANGUAGE_DETECT, row['country'], row['subject'], pt_lemas)
            for lemma in lemmas:
               update_dict(lemma, row['unique_open_rate']*100)
    write_to_dict(dictionary)