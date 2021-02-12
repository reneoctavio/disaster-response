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
2. Run `flask run --no-debugger`
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

### Train the spaCy + RoBERTa Transformer model

1. Make sure you have a GPU (it will take a very very long time on a CPU)
2. Make sure you have have installed spaCy with GPU support
3. Go to `models/spacy` folder
4. Run `spacy project run all`

## Screenshot

![WebApp](screenshots/disaster_response_1.png?raw=true)

## Project Structure
1. `api`
   - `react_app`: static files for Application (took from `build` folder created after `yarn build` in the `app` folder)
   - `app.py`: contains API functions, also serves the static files
   - `download_model.py`: helper function to download model
2. `app`
   - `public`: folder for public content
   - `src`
      - `App.*`: main application layout
      - `Classifier.*`: input box and box with classification labels
      - `UpperBar.*`: the upper bar
      - `Overview.*`: a table with graphs about properties of the dataset
3. `data`
   - `DisasterResponse.db`: a SQLite db with cleaned data, saved in the `dataset` table
   - `disaster_categories.csv`: the raw disaster categories data
   - `disaster_messages.csv`: the raw disaster messages data
   - `process_data.py`: an ETL script for reading the raw data, transform it and save into SQLite db
4. `models`
   - `nlp.py`: helper functions for cleaning a text for classification
   - `train_classifier.py`: script for creating and training a model
   - `spacy`
      - `configs\roberta.cfg`: a spaCy configuration file of a model
      - `script\convert_corpus.py`: a script that takes the SQLite DB and transform it for use in spaCy
      - `project.yml`: spaCy project configuration file
   

## Acknowledgments
- [spaCy](https://spacy.io) for building the classification network with transformers
- [spaCy tranformers](https://github.com/explosion/spacy-transformers) for loading transformers into model
- [spaCy projects](https://github.com/explosion/projects) for providing examples of spaCy projects
- [Hugging Face](https://huggingface.co/roberta-base) for providing the RoBERTa transformer model
- [Create React App](https://github.com/facebook/create-react-app) for providing the template for Web Application
- [Material UI](https://material-ui.com) for providing a framework for the React Application
- [Scikit-learn](https://scikit-learn.org/stable/) for providing machine learning tools
- [NLTK](https://www.nltk.org) for providing several natural language processing tools
- [Flask](https://flask.palletsprojects.com/) for providing the framework to create an API that serves the Web Application
