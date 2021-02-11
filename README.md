# Disaster Response Pipeline Project

- This projects creates an webapp that helps classifying messsages for Disater Response.
- The dataset is from [Figure Eight](https://appen.com/datasets/combined-disaster-response-data/)
- The webapp front-end used React, and the back-end, Flask.
- We created two models, one using sklearn and nltk, the other using spaCy and transformers.

## Instructions:

### Install required libraries

1. `pip install -r requirements.txt`

### Just use the App

1. Go to api directory `cd api`
2. Run `gunicorn --bind 0.0.0.0:5000 app:app`
3. It will take a while to download the almost 500MB spaCy model
4. Go to http://0.0.0.0:5000/
5. Then you can test messages

### Run the ETL and ML pipelines

1. Run the following commands in the project's root directory to set up your database and model.
2. To run ETL pipeline that cleans data and stores in database
   - `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
3. To run ML pipeline that trains classifier and saves
   - `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

### Build React App

1. Go to app dir
2. Make sure you have Node.js and yarn installed
3. `yarn build`

### Train the spaCy + roBERTa Transformer model

1. Make sure you have a GPU (it will take a very very long time on a CPU)
2. Make sure you have have installed spaCy with GPU support
3. Go to `models/spacy` folder
4. Run `spacy project run all`

## Screenshot

![WebApp](screenshots/disaster_response_1.png?raw=true)
