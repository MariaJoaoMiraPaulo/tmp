import csv
from langdetect import detect, detect_langs
from preprocessing.utils import get_data, discard_subject
from preprocessing.dictionary_assembler import clean_subject

def main():
    table = get_data()
    filename = 'data/lang_analysis.csv'
    with open(filename, 'w') as incsvfile:
        writer = csv.writer(incsvfile)
        for row in table:
            if not discard_subject(row.subject, row.unique_open_rate, row.country):
                try:
                    subject = clean_subject(row.subject)
                    language = detect_langs(row.subject)
                    if language[0].prob >= 0.5:
                        writer.writerow([row.country]+[language[0].lang])
                except:
                    continue
    print("CSV file updated with success.")



if __name__ == '__main__':
    main()