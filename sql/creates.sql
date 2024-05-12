CREATE TABLE Baskets (
    id INT PRIMARY KEY
);

CREATE TABLE Accounts (
    id INT PRIMARY KEY,
    email VARCHAR(255),
    password VARCHAR(255),
    basket_id INT,
    FOREIGN KEY (basket_id) REFERENCES Baskets(id)
);

CREATE TABLE Addresses (
    id INT PRIMARY KEY,
    street VARCHAR(255),
    city VARCHAR(100),
    postal_code VARCHAR(10),
    country VARCHAR(100)
);

CREATE TABLE Departments (
    id INT PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE JobPositions (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES Departments(id)
);

CREATE TABLE Employees (
    id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    salary DECIMAL(10, 2),
    job_position_id INT,
    -- superior_id INT,
    FOREIGN KEY (job_position_id) REFERENCES JobPositions(id)
    -- FOREIGN KEY (superior_id) REFERENCES Employees(id)
    
);

CREATE TABLE Patients (
    id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    PESEL VARCHAR(11),
    account_id INT,
    address_id INT,
    FOREIGN KEY (account_id) REFERENCES Accounts(id),
    FOREIGN KEY (address_id) REFERENCES Addresses(id)
);

CREATE TABLE Prescriptions (
    id INT PRIMARY KEY,
    code INT,
    issuance_date DATE,
    patient_id INT,
    FOREIGN KEY (patient_id) REFERENCES Patients(id)
);

CREATE TABLE Orders (
    id INT PRIMARY KEY,
    order_date DATE,
    receipt_date DATE,--data odbioru
    patient_id INT,
    employee_id INT,
    FOREIGN KEY (patient_id) REFERENCES Patients(id),
    FOREIGN KEY (employee_id) REFERENCES Employees(id)
);

CREATE TABLE Pharmacies (
    id INT PRIMARY KEY,
    address_id INT,
    FOREIGN KEY (address_id) REFERENCES Addresses(id)
);

CREATE TABLE Products (
    id INT PRIMARY KEY,
    name VARCHAR(40),
    ptype VARCHAR(20),
    price INT,
    manufacturer VARCHAR(30)
);

CREATE TABLE Prescriptions_Products (
    prescription_id INT,
    product_id INT,
    product_amount INT,
    PRIMARY KEY (prescription_id, product_id),
    FOREIGN KEY (prescription_id) REFERENCES Prescriptions(id),
    FOREIGN KEY (product_id) REFERENCES Products(id)
);

CREATE TABLE Storages (
    id INT PRIMARY KEY,
    address_id INT,
    FOREIGN KEY (address_id) REFERENCES Addresses(id)
);

CREATE TABLE Storages_Products (
    storage_id INT,
    product_id INT,
    product_amount INT,
    PRIMARY KEY (storage_id, product_id),
    FOREIGN KEY (storage_id) REFERENCES Storages(id),
    FOREIGN KEY (product_id) REFERENCES Products(id)
);

CREATE TABLE Orders_Products (
    order_id INT,
    product_id INT,
    product_amount INT,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES Orders(id),
    FOREIGN KEY (product_id) REFERENCES Products(id)
);

CREATE TABLE BasketElement (
    id INT PRIMARY KEY,
    product_amount INT,
    product_id INT,
    basket_id INT,
    FOREIGN KEY (product_id) REFERENCES Products(id),
    FOREIGN KEY (basket_id) REFERENCES Baskets(id)
);

CREATE TABLE Pharmacies_Products (
    pharmacy_id INT,
    product_id INT,
    product_amount INT,
    PRIMARY KEY (pharmacy_id, product_id),
    FOREIGN KEY (pharmacy_id) REFERENCES Pharmacies(id),
    FOREIGN KEY (product_id) REFERENCES Products(id)
);