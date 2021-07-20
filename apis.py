import requests
import pandas as pd
import sqlalchemy
import os
import random
from sqlalchemy import create_engine


def get_data_from_api(base_url):

    response = requests.get(base_url)
    response_json = response.json()
    results = response_json['results']
    return results


def get_data_items(results):
    # data items to be used
    category = results['category']
    question_type = results['type']
    difficulty = results['difficulty']
    question = results['question']
    correct_answer = results['correct_answer']
    incorrect_answers_list = results['incorrect_answers']  # this is a list
    if len(incorrect_answers_list) == 1:
        incorrect_answers = incorrect_answers_list[0]
        answer_choices = 'True, False'
    else:
        incorrect_answers = incorrect_answers_list[0] + ', ' +\
            incorrect_answers_list[1] + ', ' +\
            incorrect_answers_list[2]

        # storing all answer choices in a random order
        answer_choices_list = incorrect_answers_list
        answer_choices_list.append(correct_answer)
        random.shuffle(answer_choices_list)
        answer_choices = answer_choices_list[0] + ', ' +\
                         answer_choices_list[1] + ', ' +\
                         answer_choices_list[2] + ', ' +\
                         answer_choices_list[3]

    return category, question_type, difficulty, question, correct_answer,\
        incorrect_answers, answer_choices


def create_dataframe():
    col_names = ['Category', 'Question Type', 'Difficulty', 'Question',
                 'Correct Answer', 'Incorrect Answer(s)', 'Answer Choices']
    dataframe = pd.DataFrame(columns=col_names)
    return dataframe


def put_values_dataframe(dataframe, values):
    dataframe.loc[len(dataframe.index)] = values
    return dataframe


def create_engine_function(dbName):
    # Create an engine
    return create_engine('mysql://root:codio@localhost/'
                         + dbName + '?charset=utf8', encoding='utf-8')


def save_data_to_file(dtfr, dbName, tableName, fileName):
    dtfr.to_sql(tableName, con=create_engine_function(dbName),
                if_exists='replace', index=False)
    os.system('mysqldump -u root -pcodio {} > {}.sql'.format(dbName, fileName))


def load_database(dbName, fileName):
    os.system('mysql -u root -pcodio -e "CREATE DATABASE IF NOT EXISTS '
              + dbName + '; "')
    os.system('mysql -u root -pcodio ' + dbName + ' < ' + fileName + '.sql')


def main():
    # defining some terms
    tableName = 'allquizzes'
    fileName = 'quiz_file'
    dbName = 'quiz_db'

    base_url = 'https://opentdb.com/api.php?amount=50'

    # explore the session_token option to get unique questions
    # session_token = '12286e9bb10cfcfa9ea7597f1ee68cdd'

    load_database(dbName, fileName)
    dtfr_initial = pd.read_sql_table(tableName,
                                     con=create_engine_function(dbName))

    results = get_data_from_api(base_url)
    for question in results:
        values = get_data_items(question)
        # print(values)

        # create a new dataframe/database/SQL file
        # dataframe = create_dataframe()

        dtfr_final = put_values_dataframe(dtfr_initial, values)
        save_data_to_file(dtfr_final, dbName, tableName, fileName)

    print(dtfr_final.tail(1))


if __name__ == "__main__":
    main()
