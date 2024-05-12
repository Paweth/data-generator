import getpass
import oracledb
import itertools
import os

from itertools import permutations
from io import *

from database_context import * 
from tables import *

# def filter_permutations(permutations, pkey_pairs):
#     new_tset = ()
#     for t1 in permutations:
#         flag = True
#         for t2 in pkey_pairs:
#             if t1[0] == t2[0] and t1[1] == t2[1]:
#                 print(f"t1: {t1}")
#                 flag = False
#             else:
#                 pass
#         if flag == True:
#             new_tset += (t1,)
#     return new_tset

# or PermutationContext -> context for creating successive permutations
class PermutationState:
    def __init__(self):
        self.min_lkey = 0 # last used id for permutation (left key)
        self.min_rkey = 0 # --||-- (right key)
        self.permutations : Set[int, Tuple[int,int]] = set()
    def __getattr__(self, attrib):
        return self.permutations.__getattribute__(attrib)
    def init(self):
        pass

class DataGenerator:
    def __init__(self):
        self.tables : List[Table] = []
        self.tables.append(Baskets())
        self.tables.append(Accounts())
        self.tables.append(Addresses())
        self.tables.append(Departments())
        self.tables.append(JobPositions())
        self.tables.append(Employees())
        self.tables.append(Patients())
        self.tables.append(Prescriptions())
        self.tables.append(Orders())
        self.tables.append(Pharmacies())
        self.tables.append(Products())
        self.tables.append(Prescriptions_Products())
        self.tables.append(Storages())
        self.tables.append(Storages_Products())
        self.tables.append(Orders_Products())
        self.tables.append(BasketElement())
        self.tables.append(Pharmacies_Products())

        self.db_context : DatabaseContext = DatabaseContext()
        self.gen_context : GeneratorContext = GeneratorContext()

        self.db_context.connect()
        self.collect_data()

    def collect_data(self):
        for t in self.tables:
            if t.is_join_table():
                self.gen_context.existing_key_pairs[t.name] = set()   
                self.gen_context.tables_max_id[t.name] = set()

                key : ColumnDefinition = t.get_pkeys()
                q1 = f"select max(id) from {key.referenced_table[0].__name__}"
                r1, _ = self.db_context.execute_query(q1)

                q2 = f"select max(id) from {key.referenced_table[1].__name__}"
                r2, _ = self.db_context.execute_query(q2)

                if len(r1) > 0 and len(r2) > 0:
                    query_string = f"select {key.name[0]}, {key.name[1]} from {t.name}"
                    existing_keys, _ = self.db_context.execute_query(query_string)
                    self.gen_context.existing_key_pairs[t.name].update(set(existing_keys)) 
                    self.gen_context.tables_max_id[t.name].add((r1[0][0], r2[0][0]))
            else:
                query_string = f"select count(*) from {t.name}"
                result, _ = self.db_context.execute_query(query_string)
                self.gen_context.tables_max_id[t.name] = int(result[0][0])

    def generate_sql_statements(self, query_template : str, rows):
        statements : List[str] = []
        for row in rows:
            full_query = query_template
            for i,c in enumerate(row):
                if type(c) == str:
                    full_query = full_query.replace(f":{i + 1}", "\'" + str(c) + "\'")
                else:
                    full_query = full_query.replace(f":{i + 1}", str(c))
            statements.append(full_query)
        return statements

    def write_to_file(self, text):
        directory_path = "./generated_sql"
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        with open(f"{directory_path}/inserts.sql", "a") as file:
            file.write(text)
            file.write("\n") 

    def generate_table_data(self, amount, table : Table):
        print(table.name)
        rows = []
        for _ in range(amount):
            rows.append(table.generate_row(self.gen_context))
        query_template = f"insert into {table.name} values ({",".join([f":{x}" for x in range(1,len(rows[0]) + 1)])})\n"
        with self.db_context.connection.cursor() as cursor:
            cursor.executemany(query_template, rows)
        self.db_context.connection.commit()
        res = self.generate_sql_statements(query_template, rows)
        queries = "".join(res)
        self.write_to_file(queries)

    def generate_data(self, amount):
        for table in self.tables:
            self.generate_table_data(amount, table)
        
