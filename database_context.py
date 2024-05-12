import oracledb
import json
import os.path
from getpass import getpass

def provide_data(fields, data): # mutating data
    for f in fields:
        val = ""
        if f == "user":
            print("Provide username:")
            val = input()
        elif f == "password":
            val = getpass("Provide password for database user:")
        elif f == "host":
            print("Provide host ip address:")
            val = input()
        elif f == "port":
            print("Provide port number:")
            val = input()
        elif f == "service_name":
            print("Provide service name:")
            val = input()        
        data[f] = val

class DatabaseContext:
    def __init__(self):
        self.is_connected = False
        self.is_defined = False
        self.connection = 0
    def connect(self):
        data = {}
        fields = ["user","password","host","port","service_name"]
        file_path = "./connection.json"
        if os.path.isfile(file_path):
            f = open(file_path)
            data = json.load(f)
            lacking_fields = []
            for f in fields:
                if f not in data:
                    lacking_fields.append(f)
            provide_data(lacking_fields, data)
        else:
            provide_data(fields, data)
        try:
            self.connection = oracledb.connect(
                user=data["user"],
                password=data["password"],
                host=data["host"],
                port=data["port"],
                service_name=data["service_name"])
            self.is_connected = True
        except oracledb.Error as error:
            print("Oracle Database Error:", error)
    def execute_query(self, query_string):
        assert(self.is_connected)
        cursor = self.connection.cursor()
        cursor.execute(query_string)
        if cursor.rowcount == -1:
            print("Error fetching data:", cursor.getbatcherrors())
        return (cursor.fetchall(), cursor.rowcount)
    
def test_connection():
    db_context = DatabaseContext()
    db_context.connect()
    print("Connected")
    res = db_context.execute_query("select * from Employees fetch next 10 rows only")
    print(res)
    
if __name__ == "__main__":
    test_connection()