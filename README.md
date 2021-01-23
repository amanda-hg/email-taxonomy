<center><u><h1>Email Taxonomy</h1></u></center>

## 1. Índice

1. Index
2. Introduction
3. Folder structure
4. Parameters
    * 4.1 Configuration file
    * 4.2 Input data
5. Results
6. Execution

## 2. Introduction
Email Taxonomy is a natural language processing application, which is responsible for classifying emails and analyzing their main topics.

## 3. Folder structure
```python
email-taxonomy
    |
    |-------- config/
    |              |-------- config.json
    |
    |-------- code/
    |
    |-------- data/
    |             |-------- enron-dataset.csv
    |
    |-------- logs/
    |
    |-------- output/
    |            |-------- model_trained/
    |
    |-------- tmp/
```

For the application to work, this folder structure must be respected.

** Note:** \
In the tmp/ folder, temporary data files will be created for all the executions the dataset goes through.
In the model_trained/ will save the LDA model.

## 4. Parameters

### 4.1 Configuration file

The `config.json` file should be located in the `config` folder

#### Required variables

    "train": (boolean) variable to indicate to train an LDA model.
    "predict": (boolean) variable to indicate to make a prediction about that model.
    "n_top_words": (integer) number of n top words of each topic.

### 4.2 Input data

An input file is required, a csv containing the email information. In this case:
* **enron_05_17_2015_with_labels_v2_100K_chunk_1_of_6.csv**: dataset with the emails of Enron company employees.

## 5. Results

Among the results, three files are saved:
1) The LDA model.
2) The Count Vectorizer model
3) An excel with the most relevant words of each topic.

## 6. Execution

Python version 3.8.0 has been used for this application. To run this project, you just have to go to the root of the project and run the following line of code:

```python
python3.8 code/main_app.py
```