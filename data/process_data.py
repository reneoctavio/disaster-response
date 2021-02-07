import re
import sys

import pandas as pd

from sqlalchemy import create_engine


def load_data(messages_file: str, categories_file: str) -> pd.DataFrame:
    """Read the dataset messages and categories files"""
    messages = pd.read_csv(messages_file)
    categories = pd.read_csv(categories_file)
    return messages.merge(categories, on="id")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the data"""

    # Split categories into separate columns
    categories = df["categories"].str.split(";", expand=True)

    # Get categories columns names
    row = categories.iloc[0]
    category_colnames = row.apply(lambda x: re.findall(r"(\w+)\-\d", x)[0])
    categories.columns = category_colnames

    # Get categories values
    categories = categories.applymap(lambda x: int(str(x)[-1]))
    for column in categories:
        categories[column] = pd.to_numeric(categories[column])

    # Replace old category column with new categories values
    df = df.drop("categories", axis=1)
    df = pd.concat([df, categories], axis=1)

    # Remove duplicates
    df = df.drop_duplicates()

    # Column `related` has values equal to 2
    # Change them to zero
    # They all have all categories columns equal to 0
    df.loc[df["related"] == 2, "related"] = 0

    return df


def save_data(df: pd.DataFrame, database_file: str):
    engine = create_engine(f"sqlite:///{database_file}")
    df.to_sql("dataset", engine, index=False, if_exists="replace")


def main():
    if len(sys.argv) == 4:

        # pylint: disable=unbalanced-tuple-unpacking
        messages_file, categories_file, database_file = sys.argv[1:]

        print(
            "Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}".format(
                messages_file, categories_file
            )
        )
        df = load_data(messages_file, categories_file)

        print("Cleaning data...")
        df = clean_data(df)

        print("Saving data...\n    DATABASE: {}".format(database_file))
        save_data(df, database_file)

        print("Cleaned data saved to database!")

    else:
        print(
            "Please provide the filepaths of the messages and categories "
            "datasets as the first and second argument respectively, as "
            "well as the filepath of the database to save the cleaned data "
            "to as the third argument. \n\nExample: python process_data.py "
            "disaster_messages.csv disaster_categories.csv "
            "DisasterResponse.db"
        )


if __name__ == "__main__":
    main()
