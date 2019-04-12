CREATE TABLE SUPPLIER(
    Supplier_No INTEGER PRIMARY KEY ,
    Supplier_Name VARCHAR(30) NOT NULL,
    Supplier_Contact_No VARCHAR(13) NOT NULL,
    Company_Name VARCHAR(40),
    Supplier_Address VARCHAR(100),
    Company_Contact_No VARCHAR(13)
);

CREATE TABLE CHEMICALS(
    Sno INTEGER(4)  UNIQUE,
    Chem_Name VARCHAR(50) PRIMARY KEY,
    Molecular_Formula VARCHAR(20),
    Stock_Available DECIMAL(9,3) NOT NULL
);

CREATE TABLE CHEM_ORDER(
    Sno INTEGER(3) UNIQUE ,
    C_name varchar(50),
    No_packs INTEGER(6),
    Supplied_By INTEGER,
    Order_Date Date,
    Date_of_Delivery Date,
    Order_Number INTEGER primary key,
    Price decimal(9,2),
    Total_price decimal(9,2),
    Stock_bought decimal(9,3),
    FOREIGN KEY (Supplied_By) REFERENCES SUPPLIER(Supplier_No),
    FOREIGN KEY (C_name) references CHEMICALS(Chem_Name)
);

CREATE TABLE GLASSWARE(
    Sno INTEGER UNIQUE ,
    Glass_Name VARCHAR(50) primary key,
    Capacity VARCHAR(10),
    Quantiy_Available integer(3)
);

create table GLASS_ORDER(
    Sno INTEGER(3) UNIQUE ,
    G_name varchar(50),
    Price decimal(9,3),
    Supplied_By INTEGER,
    Order_Date Date,
    Date_of_Delivery Date,
    Total_price decimal(9,3),
    No_bought integer,
    Order_Number INTEGER primary key,
    FOREIGN KEY (Supplied_By) REFERENCES SUPPLIER(Supplier_No),
    foreign key (G_name) references GLASSWARE(Glass_Name)
);


CREATE TABLE INSTRUMENT(
    Sno INTEGER(3) UNIQUE ,
    Inst_Name VARCHAR(50) primary key,
    Number_Of_Units_Present INTEGER(3)
);

create table INST_ORDER(
    Sno INTEGER(3) UNIQUE ,
    I_name varchar(50),
    Supplied_By INTEGER,
    Order_Date Date,
    Date_of_Delivery Date,
    Price decimal(9,3),
    Order_Number INTEGER primary key,
    No_bought integer,
    Total_price decimal(9,3),
    FOREIGN KEY (Supplied_By) REFERENCES SUPPLIER(Supplier_No),
    foreign key (I_name) references INST_ORDER(Inst_Name)
);
