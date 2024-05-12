import random
from typing import *

class Node:
    dependencies = []

class BasketsNode(Node):
    dependencies = []
    def __init__(self, name, dependencies):
        super().__init__()

class AccountsNode(Node):
    dependencies = [BasketsNode]

class AddressesNode(Node):
    dependencies = []

class DepartmentsNode(Node):
    dependencies = []

class JobPositionsNode(Node):
    dependencies = []

class EmployeesNode(Node):
    dependencies = [JobPositionsNode]

class PatientsNode(Node):
    dependencies = [AccountsNode, AddressesNode]

class PrescriptionsNode(Node):
    dependencies = [PatientsNode]

class OrdersNode(Node):
    dependencies = [PatientsNode, EmployeesNode]

class PharmaciesNode(Node):
    dependencies = [AddressesNode]

class ProductsNode(Node):
    dependencies = []

class Prescriptions_ProductsNode(Node):
    dependencies = [PrescriptionsNode, ProductsNode]

class StoragesNode(Node):
    dependencies = [AddressesNode]

class Storages_ProductsNode(Node):
    dependencies = [StoragesNode, ProductsNode]

class Orders_ProductsNode(Node):
    dependencies = [OrdersNode, ProductsNode]

class BasketElementsNode(Node):
    dependencies = [ProductsNode, BasketsNode]

class Pharmacies_ProductsNode(Node):
    dependencies = [PharmaciesNode, ProductsNode]


def compare_lists(list1, list2):
    for l1, l2 in zip(list1, list2):
        if l1 != l2:
            return False
    return True

# check if dependencies of table are in dependency list
def dependencies_inclusion(table : Node, ordered_tables):
    for dep in table.dependencies:
        if dep not in ordered_tables:
            return False
    return True

# is table a dependency of any other table
def has_dependency(table):
    if len(table.dependencies) == 0:
        return False
    return True

# TODO: check if length of ordered_tables change between while iterations (to detect cycle?)
def determine_correct_order(tables):
    ordered_tables : List[Node] = []
    while len(ordered_tables) != len(tables):
        for t in tables:
            res = has_dependency(t)
            if res == False:
                if t not in ordered_tables:
                    ordered_tables.append(t)
            elif dependencies_inclusion(t, ordered_tables):
                if t not in ordered_tables:
                    ordered_tables.append(t)
    return ordered_tables

def test_solver():
    tables : List[Node] = []

    tables.append(BasketsNode)
    tables.append(AccountsNode)
    tables.append(AddressesNode)
    tables.append(DepartmentsNode)
    tables.append(JobPositionsNode)
    tables.append(EmployeesNode)
    tables.append(PatientsNode)
    tables.append(PrescriptionsNode)
    tables.append(OrdersNode)
    tables.append(PharmaciesNode)
    tables.append(ProductsNode)
    tables.append(Prescriptions_ProductsNode)
    tables.append(StoragesNode)
    tables.append(Storages_ProductsNode)
    tables.append(Orders_ProductsNode)
    tables.append(BasketElementsNode)
    tables.append(Pharmacies_ProductsNode)

    print("\BEFORE SHUFFLE:")
    for t in tables:
        print(t.__name__)

    random.shuffle(tables)

    print("\nAFTER SHUFFLE:")

    for t in tables:
        print(t.__name__)

    ordered_tables = determine_correct_order(tables)

    print("\nAFTER SORTING")
    for t in ordered_tables:
        print(t.__name__)

if __name__ == "__main__":
    test_solver()