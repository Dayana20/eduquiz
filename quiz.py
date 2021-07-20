import pandas as pd
from apis import create_dataframe, create_engine_function, load_database
from apis import save_data_to_file


def list_categories(dataframe):
    categories = sorted(list(dataframe['Category'].unique()))
    return categories


def render_quiz(dataframe, category, difficulty):
    quiz_df = dataframe[(dataframe['Category'] == category) &
                        (dataframe['Difficulty'] == difficulty)]
    random_quiz = quiz_df.sample(2)
    for index, row in random_quiz.iterrows():
        if row['Question Type'] == 'boolean':
            print("         Answer the following question! (True or False)")
            print('         ----------------------------------------------')
            print(row['Question'])
            user_answer = input()
            if user_answer == row['Correct Answer']:
                print("You got it right!")
            else:
                print("That is not correct!")
        else:
            print("         Answer the following multiple choice question!")
            print('         ----------------------------------------------')
            print(row['Question'])
            print("         Below are the answer choices")
            print('         ----------------------------')
            print(row['Answer Choices'])
            user_answer = input()
            if user_answer == row['Correct Answer']:
                print("You got it right!")
            else:
                print("That is not correct!")

    return random_quiz


def main():
    # defining some terms
    tableName = 'allquizzes'
    fileName = 'quiz_file'
    dbName = 'quiz_db'

    load_database(dbName, fileName)
    dataframe = pd.read_sql_table(tableName,
                                  con=create_engine_function(dbName))

    # we have 24 unique categories in our database
    # print(dataframe['Category'].nunique())

    # we have 39 questions of type History
    # we have 6 questions of type Celebrities
    # print(dataframe[dataframe['Category'] == 'History'].count())

    # list all the available categories and ask user for the category
    # and difficulty level they would like
    print('         Below are the categories that you can choose from!')
    print('         --------------------------------------------------')
    print(list_categories(dataframe))
    category = input('What category would you like to test yourself on? ')
    difficulty = input(
        'What difficulty level would you like (easy, medium, or hard)? ')

    print(render_quiz(dataframe, category, difficulty))


if __name__ == "__main__":
    main()
