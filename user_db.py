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


def new_user(id, username):
    tableName = 'user_data'
    fileName = 'user_file'
    dbName = 'quiz_db'
    if id == 1:
        dataframe = create_dataframe()
    else:
        dataframe = db_to_dataframe(dbName, tableName, fileName)
    dataframe.loc[len(dataframe.index)] = (id, username, 0, 0, 0)
    save_data_to_file(dataframe, dbName, tableName, fileName)
    print(dataframe.tail(1))


def main():
    # defining some terms
    create_dataframe()


if __name__ == "__main__":
    main()
