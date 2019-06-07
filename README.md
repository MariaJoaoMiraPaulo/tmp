# Subject Analyzer

A predictive model for classifying a subject field regarding its quality. Based on the amount of data collected by E-goi and available for use, it is intended to develop a classification model capable of receiving a subject and retrieving a quality, between 1 to 5 stars. The subject is analyzed, not only in a morphological way but also semantically. 

## How? 

- The **morphological** assembler computes morphological features, taking into consideration the number of words, number of chars, case percentage, the presence of punctuation, prefixes, emojis, personalization, special_chars, numbers, and currency. 
- The **semantic** assembler computes semantic features, analyzing the past performance of each word presented in the subject, based on a created dictionary.

**The morphological and semantic features, the country and the business sector will serve as an input for the predictive model.**

## Instalation

1. Clone this repo 

2. Create image and run docker container

    `make container && make run`

## Getting started

1. API Documenation

    [API Documentation](http://127.0.0.1:5000/)

2. Classify subject 

   `cd src && python main.py classify -c portugal -s Marketing -subject Melhores descontos, aproveita!`
   

    > - **c**: country name
    > - **s**: sector name
    > - **subject**: subject to be analyzed

3. Train the model 

    `cd src && python main.py train`

4. Evaluate the model 

    `cd src && python main.py evaluate`






