import csv, sys, emoji, re, math, argparse
from emoji import UNICODE_EMOJI
from enum import Enum

def main():
    parser = argparse.ArgumentParser('Classify a subject regarding the morphology.')
    parser.add_argument("subject", type=str, nargs='*', help="Subject")
    args = parser.parse_args()

    subject = ' '.join(args.subject)
    print("[nr_words, nr_chars, case_percentage, punctuation, prefix, emojis, personalization, special_chars, numbers, currency]")
    print(subject_analyzer(subject))

def get_number_words(subject: str):
    """Returns the number of words contained in a subject.

    Args:
        subject: subject to be analyzed.
    
    Returns: 
        int: number of words.

    """
    return len(subject.split())

def get_number_chars(subject: str):
    """Returns the number of characters contained in a subject.

    Args:
        subject: subject to be analyzed.

    Returns: 
        int: number of characters
    """
    return len(subject)

def get_case_percentage(subject: str):
    """Returns the percentage of upper case in a subject.

    Args:
        subject: subject to be analyzed.
    
    Returns: 
        float: case percentage.

    """
    if len(subject) == 0: return 0
    caps_characters = 0
    for character in subject:
        if character.isupper():
            caps_characters += 1
    return (caps_characters / len(subject))*100

def contains_emoji(subject: str):
    """Returns true if the subject contains at least one emoji or false if the subject does not contain emojis.

    Args:
        subject: subject to be analyzed.

    Returns: 
        True if the subject has emojis, False otherwise.

    """
    return any(char in UNICODE_EMOJI for char in subject)

def contains_punctuation(subject: str):
    """Returns true if the subject contains at least one punctuation mark or false if the subject does not contain any punctuation.

    Args:
        subject: subject to be analyzed.

    Returns: 
        True if the subject has punctuation, False otherwise.

    """
    return bool(re.search('[!?]( |$)', subject))

def contains_prefixes(subject: str):
    """Returns true if the subject contains at least one prefix code or false if the subject does not contain any prefix code.

    Args:
        subject: subject to be analyzed.

    Returns: 
       True if the subject has prefixes, False otherwise.

    """
    subject_prefixes = ['RE', 'FW', 'FWD', 'ACTION', 'WAS', 'FYI', 'NRN', 'OT', 'EOM', 'WFH', '1L', 'NONB', 'ASAP']
    subject = subject.upper()    
    return any(subject.startswith(prefix + ':') for prefix in subject_prefixes) 

def contains_number(subject: str):
    """Returns true if the subject contains at least one number or false if the subject does not contain any number.

    Args:
        subject: subject to be analyzed.
    
    Returns: 
       True if the subject has numbers, False otherwise.

    """
    return any (char.isdigit() for char in subject)

def contains_special_chars(subject: str):
    """Returns true if the subject contains at least one prefix code or false if the subject does not contain any prefix code.

    Args:
        subject: subject to be analyzed.
    
    Returns: 
        True if the subject has special chars, False otherwise.

    """
    words = subject.split()
    return any(not word.isalnum() and not bool(re.search('[!?€£$]', word)) and word not in UNICODE_EMOJI for word in words)

def contains_personalizaton(subject: str):
    """Returns true if the subject contains at least one personalization code or false if the subject does not contain any prefix code.

    Args:
        subject: subject to be analyzed.
    
    Returns: 
        True if the subject has personalization, False otherwise.

    """
    personalization_codes = ['!fname', '!fullname', '!email', '!lname', '!birth_date', '!extra_field_1101', '!telephone', '!cellphone']
    return any(code in subject for code in personalization_codes)

def contains_any_currency(subject: str):
    """Returns true if the subject contains at least a currency reference, symbol or abbreviation, or false if the subject does not contain any currency reference.

    Args:
        subject: subject to be analyzed.
    
    Returns: 
        True if the subject has currency, False otherwise.

    """
    return bool(re.search(r'(?i)((eur+((o)s*)*( |\b))|reais( |\b))|[$£€]|R\$', subject))

def subject_analyzer(subject: str):
    """Returns a list with all structural features.

    Args:
        subject: subject to be analyzed.

    Returns:
        list: list of features.

    """
    return [get_number_words(subject), get_number_chars(subject), int(get_case_percentage(subject)), int(contains_punctuation(subject)), int(contains_prefixes(subject)), int(contains_emoji(subject)), int(contains_personalizaton(subject)), int(contains_special_chars(subject)), int(contains_number(subject)), int(contains_any_currency(subject))]

if __name__ == '__main__':
    main()  

