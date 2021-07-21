# from script import User 
import pandas as pd
from apis import create_engine_function, save_data_to_file, load_database


# here, was trying to figure out how to get access to user ids
# user_1 = User.query.filter_by(username='holla').first()
# print(user_1.id)


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
    print(dtfr_final.tail(1))


def main():
    # defining some terms
    create_dataframe()


if __name__ == "__main__":
    main()
