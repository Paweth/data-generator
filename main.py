import random
from column_types import *
from data_generator import *
from tables import *

from dependency_solver import *

# DatabaseGenerator
# databaseConnectionContext
# if column is fkey or pkey generate values yourself (IdType ?)
# 

# def generate(db_generator : DataGenerator):
#     tables = db_generator.tables
#     input()
    # for t in tables:

def start():
    db_generator = DataGenerator()
    tables = db_generator.tables
    while True:
        print("Choose table to generate data to (default: 0):")
        print("-1. Exit application")
        print("0. All tables")
        for i, t in enumerate(db_generator.tables):
            print(f"{i + 1}: {t.name}")
        print()
        index =  input()
        try:
            index = int(index)
        except ValueError:
            index = 0

        # assert(index >= -1 and index <= 17)
        if index < -1 or index > 17:
            print("Not valid option")
            continue
        if index == -1:
            break
        else:
            print("How many rows to generate?")
        row_number = 0
        row_number = int(input())
        assert(row_number > 0)
        if index == 0:
            db_generator.generate_data(row_number)
        else: # specific table
            index = index - 1
            db_generator.generate_table_data(row_number, tables[index])

    print("Close application")

def main():
    start()

if __name__ == "__main__":
    main()
