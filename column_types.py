from datetime import datetime, timedelta

import random
import string

lowercase = list(string.ascii_lowercase)
uppercase = list(string.ascii_uppercase)
digits = list(string.digits)
punctuation = ["$","@","%","^","&", "*"]

# ALL DATA TYPES:
# StringData, IntData
# IdData, EmailData, PasswordData
# CityData, StreetData, CountryData
# PostalCodeData, DepartmentNameData
# JobPositionNameData, FirstNameData
# LastNameData, SalaryData, PESEL_Data
# DateData, ProductNameData, ProductTypeData
# PriceData, ManufacturerData, ProductAmountData


# GENERIC DataTypes
class StringData:
    def __init__(self, max_length, min_length = -1):
        assert(max_length > min_length)
        self.max_length = max_length
        self.min_length = min_length
    def random_value(self):
        length = 0
        # print(f"string min length: {self.min_length}")
        if self.min_length < 0:
            length = self.max_length
        else:
            length = random.randrange(self.min_length, self.max_length)
        string = []
        for i in range(length):
            if i == 0:
                string.append(random.choice(uppercase))
            else:
                string.append(random.choice(lowercase))
        return "".join(string)

class IntData:
    def __init__(self, max_number, min_number = 1):
        self.max_number = max_number
        self.min_number = min_number
    def random_value(self):
        return random.randint(self.min_number, self.max_number)

class IdData(IntData):
    def __init__(self):
        super().__init__(1000000,0)

# ACCOUNTS
class EmailData(StringData):
    def __init__(self):
        super().__init__(30)
    def random_value(self):
        domains = ["google.com", "onet.pl"]
        for i, d in enumerate(domains):
            domains[i] = "@" + d
        chosen_domain = random.choice(domains)
        front_length =  self.max_length - len(chosen_domain)
        front = ""
        if random.randint(1,2) == 1:
            front = "".join([random.choice(lowercase + digits) for _ in range(random.randrange(3, front_length))])
        else:
            part_length = (front_length - 1) // 2
            front = [random.choice(lowercase + digits) for _ in range(random.randrange(1, part_length))]
            front.append(".")
            front = front + [random.choice(lowercase + digits) for _ in range(random.randrange(1, part_length))]
            front = "".join(front)
        return front + chosen_domain

        
class PasswordData:
    def random_value(self):
        password = []
        length = random.randrange(3, 10)
        character_list = []
        character_list += lowercase
        character_list += uppercase
        character_list += digits
        character_list += punctuation
        for i in range(length):
            password.append(random.choice(character_list))
        return "".join(password)


# ADDRESSES

class CityData:
    options = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego","Dallas", "San Jose", "Austin", "Jacksonville", "San Francisco", "Columbus", "Fort Worth", "Indianapolis","Charlotte", "Seattle", "Denver", "Washington", "Boston", "El Paso", "Nashville", "Detroit", "Oklahoma City","Portland", "Las Vegas", "Memphis", "Louisville"]
    def random_value(self):
        return random.choice(self.options) 

class StreetData:
    options = ["Oak Street", "Main Street", "Maple Avenue", "Park Avenue", "Cedar Road", "Pine Street", "Elm Street", "Willow Lane", "Spruce Drive", "Birch Street", "Cherry Lane", "Forest Road", "Hickory Lane", "Sycamore Street", "Poplar Avenue", "Juniper Drive", "Cypress Lane", "Magnolia Court", "Chestnut Street", "Locust Avenue", "Mulberry Lane", "Aspen Drive", "Palm Boulevard", "River Road", "Sunset Boulevard", "Washington Street", "Broadway", "High Street", "King Street", "Queen Street"]
    def random_value(self):
        return random.choice(self.options)


class CountryData:
    options = ["United States", "Canada", "United Kingdom", "Australia", "Germany", "France", "Japan", "Brazil", "India", "China", "Russia", "South Africa", "Mexico"] 
    def random_value(self):
        return random.choice(self.options)

class PostalCodeData:
    def random_value(self):
        value = ""
        value += str(random.randint(10,100))
        value += "-"
        value += str(random.randint(100,1000))
        return value


# DEPARTMENTS
class DepartmentNameData:
    options = ["Sales", "Marketing", "Human Resources", "Finance", "Engineering", "Customer Service", "Research and Development", "Information Technology", "Operations", "Legal", "Administration", "Product Management", "Quality Assurance","Supply Chain", "Public Relations", "Accounting"]
    def random_value(self):
        return random.choice(self.options)
# JOB POSITIONS
class JobPositionNameData:#depends on department
    options = {
        "Sales": ["Sales Manager", "Sales Representative", "Account Manager"], 
        "Marketing": ["Social Media Manager", "Marketing Analyst", "Brand Manager"], 
        "Human Resources": ["Employee Relations Manager", "HR Manager", "Recruiter"], 
        "Finance": ["Accountant", "Financial Analyst", "Financial Planner"], 
        "Engineering": ["Biomedical Engineer", "Chemical Engineer", "Software Engineer"], 
        "Customer Service": ["Call Center Representative", "Customer Service Manager", "Technical Support"], 
        "Research and Development": ["Scientist", "Laboratory Technician", "Research Engineer"], 
        "Information Technology": ["Systems Analyst", "Network Engineer", "IT Manager"], 
        "Operations": ["Operations Analyst", "Operations Coordinator", "Process Analyst"], 
        "Legal": ["Legal Secretary", "Compliance Officer", "General Counsel"], 
        "Administration": ["Administrative Assistant", "Receptionist", "Office Manager"], 
        "Product Management": ["Product Manager", "Product Owner", "Marketing Manager"], 
        "Quality Assurance": ["Quality Inspector", "Quality Manager", "Audit"],
        "Supply Chain": ["Logistics Analyst", "Inventory Manager", "Procurement Manager"], 
        "Public Relations": ["Brand Manager", "Public Relations Assistant", "Communications Coordinator"], 
        "Accounting": ["Bookkeeper", "Accounting Clerk", "Tax Accountant"]
    }
    def random_value(self, department_name: str = ""):
        # TODO: change so it would pick department bound to fkey
        return random.choice(self.options[random.choice(list(self.options.keys()))]) 
# EMPLOYEES
    
class FirstNameData:
    options = ["Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Henry", "Ivy", "Jack", "Katie", "Liam", "Mia", "Noah", "Olivia", "Peter", "Quinn", "Rachel", "Sam", "Taylor","Ursula", "Victor", "Wendy", "Xavier", "Yvonne", "Zachary", "Emma", "Benjamin", "Sophia", "Lucas"]
    def random_value(self):
        return random.choice(self.options)
class LastNameData:
    options = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Martinez","Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin","Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson","Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Green"]
    def random_value(self):
        return random.choice(self.options)

class SalaryData:
    def random_value(self): 
        return random.randrange(1000,9999)

# PATIENTS

class PESEL_Data:
    def random_value():
        return "".join([random.choice(digits) for _ in range(10)])
# 11 11 11 11 111

# PRESCRIPTIONS

class DateData:
    def __init__(self, start, end):
        self.min_date = start
        self.max_date = end
    def random_value(self):
        delta = self.max_date - self.min_date
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        return self.min_date + timedelta(seconds=random_second)

# PRODUCTS
class ProductNameData(StringData):
    def __init__(self):
        super().__init__(40, 3)#varchar(40)

class ProductTypeData:#varchar(30)
    options = ["Cream", "Supplement", "Medicine", "Nutrition"]
    def random_value(self):
        return random.choice(self.options)
class PriceData(IntData):
    def __init__(self):
        super().__init__(50, 3)#varchar(20)

class ManufacturerData():
    options = [
    "Johnson & Johnson",
    "Roche",
    "Novartis",
    "Merck & Co.",
    "Sanofi",
    "AstraZeneca",
    "GlaxoSmithKline (GSK)",
    "AbbVie",
    "Bayer"
]
    def random_value(self):
        return random.choice(self.options)
# PRESCRIPTIONS_PRODUCTS

class ProductAmountData(IntData):
    def __init__(self):
        super().__init__(30)


def main():
    print(lowercase)






if __name__ == "__main__":
    main()