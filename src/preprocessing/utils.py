import re
import pandas as pd
from cassandra.cluster import Cluster
from enum import Enum

ZERO_LEMMAS = 0
NR_LEMMAS = 1
LANGUAGE_DETECT = 0

class Method(Enum):
    """Specifies the different methods applied to lemmas past performance feature calculation.

    """
    AVG = 1
    WEIGHTED_AVG = 2
    MAX = 3

def get_rating(open_rate: float):
    """Converts the unique open rate into a quality class.

    Args:
        open_rate: open rate value.

    Returns:
        quality: string representing the quality class (1,2,3,4 or 5).

    """
    if open_rate >= 22.4:
        return '5'
    if open_rate >= 13.7:
        return '4'
    if open_rate >= 9.37:
        return '3'
    if open_rate >= 5.41:
        return '2'
    else:
        return '1'

def get_data():
    """Connects to cassandra cluster and returns 140000 rows from casssandra table.

    Returns:
        dataset: data rows from cassandra table.
        
    """
    cluster = Cluster(['185.79.226.211'])
    session = cluster.connect('subjectanalyzer')
    dataset = session.execute('SELECT campaign_hash, country, sector, subject, unique_open_rate from subject_data limit 140000')
    return dataset

def discard_subject(subject: str, open_rate: float, country: str):
    """Checks if the subject creates noise and so, if it should be ignored. 

    Args:
        subject: subject to be analyzed.
        open_rate: respective open rate.
        country: associated country.

    Returns:
        True if the subject should be discarded, False otherwise.

    """
    available_countries = ['portugal', 'honduras','angola','curacao', 'espanha','brasil','colombia','peru','mozambique','united_states_of_america','australia','mexico','malta', 'united_kingdom','argentina','chile']
    return bool(re.search('(\{\{IF:|\{\{FEEDBLOCK)', subject)) or open_rate > 1 or country not in available_countries

def load_dict():
    """Loads dictionary.

    Returns:
        dict: dictionary.

    """
    dictionary_frame = pd.read_csv('./data/dictionary.csv')
    return {row[0]: [row[1], row[2]] for row in dictionary_frame.values}
        