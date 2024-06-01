from tables import *

class PharmacyDatabase:
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