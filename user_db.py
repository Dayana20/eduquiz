import pandas as pd
from apis import create_engine_function, save_data_to_file, load_database


def create_dataframe():
    col_names = ['id', 'Username', 'Score', 'Quizzes Done',
                 'Questions Attempted']
    dataframe = pd.DataFrame(columns=col_names)
    return dataframe


def db_to_dataframe(dbName, tableName, fileName):
    load_database(dbName, fileName)
    dataframe = pd.read_sql_table(tableName,
                                  con=create_engine_function(dbName))
    return dataframe


def put_values_dataframe(dataframe, id, username):
    dataframe.loc[len(dataframe.index)] = (id, username, 0, 0, 0)
    return dataframe


def new_user(id, username):
    tableName = 'user_data'
    fileName = 'quiz_file'
    dbName = 'quiz_db'
    if id == 1:
        dataframe = create_dataframe()
    else:
        dataframe = db_to_dataframe(dbName, tableName, fileName)
    # dataframe.loc[len(dataframe.index)] = (id, username, 0, 0, 0)
    dtfr_final = put_values_dataframe(dataframe, id, username)
    save_data_to_file(dtfr_final, dbName, tableName, fileName)


def update_score(username, correct):
    tableName = 'user_data'
    fileName = 'quiz_file'
    dbName = 'quiz_db'
    dataframe = db_to_dataframe(dbName, tableName, fileName)

    # updating the fields in the dataframe
    if correct:
        dataframe.loc[dataframe['Username'] == username, ['Score']] += 1
    dataframe.loc[dataframe['Username'] == username, ['Quizzes Done']] += 1
    dataframe.loc[dataframe['Username'] == username,
                  ['Questions Attempted']] += 1

    # saving the new dataframe into the database
    save_data_to_file(dataframe, dbName, tableName, fileName)


def get_score(username):
    tableName = 'user_data'
    fileName = 'quiz_file'
    dbName = 'quiz_db'
    dataframe = db_to_dataframe(dbName, tableName, fileName)

    # updating the fields in the dataframe
    score = dataframe[dataframe['Username'] == username]['Score']
    quizzes_done = dataframe[dataframe['Username'] == username]['Quizzes Done']
    questions_attempted = dataframe[dataframe['Username'] == username]['Questions Attempted']
    return int(score)


if __name__ == "__main__":
    main()
