from enum import Enum 
import random
from typing import *
from column_types import *
from tables import *
from generator_context import *


# check if there are others
class Constraint(Enum):
    NONE = 0
    PKEY = 1
    COMPOSITE_PKEY = 2
    FKEY = 3

class ColumnDefinition:
    def __init__(self, name, ctype, constraint = Constraint.NONE, referenced_table = None):
        if constraint == Constraint.FKEY:
            assert referenced_table is not None
            assert issubclass(referenced_table, Table)
            assert type(ctype) == IdData
        self.name = name
        self.ctype = ctype
        self.constraint = constraint
        self.referenced_table = referenced_table
    # def generate(self, cursor):
    #     return self.type.random_value()

class Table:
    columns : List[ColumnDefinition] = []
    def __init__(self):
        self.name = type(self).__name__
    def __str__(self):
        text = f"{type(self).__name__}:\n"
        for column in self.columns:
            text += f" -> {column.name}: {column.ctype}\n"
        return text
    
    def is_join_table(self):
        counter = 0
        for column in self.columns:
            if column.constraint == Constraint.COMPOSITE_PKEY and column.referenced_table is not None:
                counter += 1
        if counter == 1:
            raise Exception("Table with only one composite pkey")
        return True if counter > 0 else False
    
    def get_pkeys(self) -> ColumnDefinition:
        pkey_columns = []
        for column in self.columns:
            if column.constraint == Constraint.COMPOSITE_PKEY or column.constraint == Constraint.PKEY:
                pkey_columns.append(column)
        return pkey_columns
        
    def generate_row(self, gen_context : GeneratorContext):
        data = [0 for _ in range(len(self.columns))]
        max_id = 0
        is_join_table = False
        index_composite_pkey_columns = {}
        for i, column in enumerate(self.columns):
            val = 0            
            column_type = type(column.ctype)
            if column_type == IdData:
                if column.constraint == Constraint.PKEY:
                    val = gen_context.tables_max_id[self.name] + 1
                    data[i] = val
                elif column.constraint == Constraint.FKEY:
                    if column.name == "superior_id":
                        # TODO add support for self-reference fkeys
                        continue
                    max_id = gen_context.tables_max_id[column.referenced_table.__name__]
                    val = random.randint(1, max_id)
                    data[i] = val
                elif self.is_join_table(): # self.is_join_table(): COMPOSITE PKEY and referenced_table
                    is_join_table = True # postpone evaluation after other members
                    index_composite_pkey_columns[i] = column

            elif column_type == JobPositionNameData: # depends on existing Department
                val = column.ctype.random_value()
                data[i] = val
            else:
                val = column.ctype.random_value()
                data[i] = val
            
        if is_join_table:
            val = []
            
            dict_iter = iter(index_composite_pkey_columns.items())
            l_index, lkey_column = next(dict_iter)
            r_index, rkey_column = next(dict_iter)
            lkey_max_id = gen_context.tables_max_id[lkey_column.referenced_table.__name__]
            rkey_max_id = gen_context.tables_max_id[rkey_column.referenced_table.__name__]

            max_id = (lkey_max_id, rkey_max_id)

            existing_keys = gen_context.existing_key_pairs[self.name]
            trial_number = 0
            while(True):
                # TODO: case when for example 99999 of 100000 possible pairs were used would take long time to find "last remaining"
                # TODO: change so it would take into account pairs that were generated (store permutations)
                assert(trial_number < 10000)
                new_pkey = (random.randint(1, lkey_max_id), random.randint(1, rkey_max_id))
                if new_pkey not in existing_keys:
                    break
                trial_number += 1
            for i, (pkey_index, _) in enumerate(index_composite_pkey_columns.items()):
                data[pkey_index] = new_pkey[i]
                
            # existing_keys.add(new_pkey)

            gen_context.tables_max_id[self.name] = (max_id[0], max_id[1]) 
        else:
            gen_context.tables_max_id[self.name] += 1
        for i, column in enumerate(self.columns):
            print(f"--> {column.name}: {data[i]}")
        print()
        return tuple(data)


class Baskets(Table):
    def __init__(self):
        super().__init__()
        self.columns = []
        self.columns.append(ColumnDefinition('id', IdData(), Constraint.PKEY)) 

class Accounts(Table):
    def __init__(self):
        super().__init__()
        self.columns = []
        self.columns.append(ColumnDefinition('id', IdData(), Constraint.PKEY))
        self.columns.append(ColumnDefinition('email', EmailData()))
        self.columns.append(ColumnDefinition('password', PasswordData()))
        self.columns.append(ColumnDefinition('basket_id', IdData(), Constraint.FKEY, Baskets))


class Addresses(Table):
    def __init__(self):
        super().__init__()
        self.columns = []
        self.columns.append(ColumnDefinition('id', IdData(), Constraint.PKEY))
        self.columns.append(ColumnDefinition('street', StreetData()))
        self.columns.append(ColumnDefinition('city', CityData()))
        self.columns.append(ColumnDefinition('postal_code', PostalCodeData()))
        self.columns.append(ColumnDefinition('country', CountryData()))

class Departments(Table):
    def __init__(self):
        super().__init__()
        self.columns = []
        self.columns.append(ColumnDefinition('id', IdData(), Constraint.PKEY))
        self.columns.append(ColumnDefinition('name', DepartmentNameData()))

class JobPositions(Table):
    def __init__(self):
        super().__init__()
        self.columns = []
        self.columns.append(ColumnDefinition('id', IdData(), Constraint.PKEY))
        self.columns.append(ColumnDefinition('name', JobPositionNameData()))
        self.columns.append(ColumnDefinition('department_id', IdData(), Constraint.FKEY, Departments))

class Employees(Table):
    def __init__(self):
        super().__init__()
        self.columns = []
        self.columns.append(ColumnDefinition('id', IdData(), Constraint.PKEY))
        self.columns.append(ColumnDefinition('first_name', FirstNameData()))
        self.columns.append(ColumnDefinition('last_name', LastNameData()))
        self.columns.append(ColumnDefinition('salary', SalaryData()))
        self.columns.append(ColumnDefinition('job_position_id', IdData(), Constraint.FKEY, JobPositions))
        # self.columns.append(ColumnDefinition('superior_id', IdData(), Constraint.FKEY, type(self)))    

class Patients(Table):
    def __init__(self):
        super().__init__()
        self.columns = []
        self.columns.append(ColumnDefinition('id', IdData(), Constraint.PKEY))
        self.columns.append(ColumnDefinition('first_name', FirstNameData()))
        self.columns.append(ColumnDefinition('last_name', LastNameData()))
        self.columns.append(ColumnDefinition('PESEL', PESEL_Data))
        self.columns.append(ColumnDefinition('account_id', IdData(), Constraint.FKEY, Accounts))    
        self.columns.append(ColumnDefinition('address_id', IdData(), Constraint.FKEY, Addresses))        

class Prescriptions(Table):
    def __init__(self):
        super().__init__()
        self.columns = []
        self.columns.append(ColumnDefinition('id', IdData(), Constraint.PKEY))
        self.columns.append(ColumnDefinition('code', IntData(100000)))
        self.columns.append(ColumnDefinition('issuance_date', DateData(datetime.strptime('1/1/2008 1:30 PM', '%m/%d/%Y %I:%M %p'),datetime.strptime('1/1/2020 4:50 AM', '%m/%d/%Y %I:%M %p'))))
        self.columns.append(ColumnDefinition('patient_id', IdData(), Constraint.FKEY, Patients))        

class Orders(Table):
    def __init__(self):
        super().__init__()
        self.columns = []
        self.columns.append(ColumnDefinition('id', IdData(), Constraint.PKEY))
        self.columns.append(ColumnDefinition('order_date', DateData(datetime.strptime('1/1/2008 1:30 PM', '%m/%d/%Y %I:%M %p'),datetime.strptime('1/1/2020 4:50 AM', '%m/%d/%Y %I:%M %p'))))
        self.columns.append(ColumnDefinition('receipt_date', DateData(datetime.strptime('1/1/2008 1:30 PM', '%m/%d/%Y %I:%M %p'),datetime.strptime('1/1/2020 4:50 AM', '%m/%d/%Y %I:%M %p'))))
        self.columns.append(ColumnDefinition('patient_id', IdData(), Constraint.FKEY, Patients))
        self.columns.append(ColumnDefinition('employee_id', IdData(), Constraint.FKEY, Employees))      

class Pharmacies(Table):
    def __init__(self):
        super().__init__()
        self.columns = []
        self.columns.append(ColumnDefinition('id', IdData(), Constraint.PKEY))
        self.columns.append(ColumnDefinition('address_id', IdData(), Constraint.FKEY, Addresses))    

class Products(Table):
    def __init__(self):
        super().__init__()
        self.columns = []
        self.columns.append(ColumnDefinition('id', IdData(), Constraint.PKEY))
        self.columns.append(ColumnDefinition('name', ProductNameData()))
        self.columns.append(ColumnDefinition('ptype', ProductTypeData()))
        self.columns.append(ColumnDefinition('price', PriceData()))
        self.columns.append(ColumnDefinition('manufacturer', ManufacturerData()))

class Prescriptions_Products(Table):
    def __init__(self):
        super().__init__()
        self.columns = []
        self.columns.append(ColumnDefinition('prescription_id', IdData(), Constraint.COMPOSITE_PKEY, Prescriptions))
        self.columns.append(ColumnDefinition('product_id', IdData(), Constraint.COMPOSITE_PKEY, Products))
        self.columns.append(ColumnDefinition('product_amount', ProductAmountData()))

class Storages(Table):
    def __init__(self):
        super().__init__()
        self.columns = []
        self.columns.append(ColumnDefinition('id', IdData(), Constraint.PKEY))
        self.columns.append(ColumnDefinition('address_id', IdData(), Constraint.FKEY, Addresses))        

class Storages_Products(Table):
    def __init__(self):
        super().__init__()
        self.columns = []
        self.columns.append(ColumnDefinition('storage_id', IdData(), Constraint.COMPOSITE_PKEY, Storages))
        self.columns.append(ColumnDefinition('product_id', IdData(), Constraint.COMPOSITE_PKEY, Products))
        self.columns.append(ColumnDefinition('product_amount', ProductAmountData()))

class Orders_Products(Table):
    def __init__(self):
        super().__init__()
        self.columns = [
            ColumnDefinition('order_id', IdData(), Constraint.COMPOSITE_PKEY, Orders),
            ColumnDefinition('product_id', IdData(), Constraint.COMPOSITE_PKEY, Products),
            ColumnDefinition('product_amount', ProductAmountData())
            ]

class BasketElement(Table):
    def __init__(self):
        super().__init__()
        self.columns = []
        self.columns.append(ColumnDefinition('id', IdData(), Constraint.PKEY))
        self.columns.append(ColumnDefinition('product_amount', ProductAmountData()))
        self.columns.append(ColumnDefinition('product_id', IdData(), Constraint.FKEY, Products))
        self.columns.append(ColumnDefinition('basket_id', IdData(), Constraint.FKEY, Baskets))

class Pharmacies_Products(Table):
    def __init__(self):
        super().__init__()
        self.columns = []
        self.columns.append(ColumnDefinition('pharmacy_id', IdData(), Constraint.COMPOSITE_PKEY, Pharmacies))
        self.columns.append(ColumnDefinition('product_id', IdData(), Constraint.COMPOSITE_PKEY, Products))
        self.columns.append(ColumnDefinition('product_amount', ProductAmountData()))

