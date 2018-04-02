import sqlite3
import csv
connection = sqlite3.connect("data/sql/adk.db")
cursor = connection.cursor()

# create patient table
sql_command = """
DROP TABLE IF EXISTS patient;
"""

cursor.execute(sql_command)

sql_command = """
CREATE TABLE IF NOT EXISTS patient (
    patient_ID VARCHAR(11) PRIMARY KEY, 
    age INTEGER,
    gender CHAR(1),
    education VARCHAR(10));"""

cursor.execute(sql_command)

# import patient info from patients.csv
with open('patients.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        sql_command = """INSERT INTO patient (patient_ID, age, gender, education) 
        VALUES ("{patient_ID}", {age}, "{gender}", "{education}");""".format(
            patient_ID = row[0],
            age = row[1],
            gender = row[2],
            education = row[3],
        )
        cursor.execute(sql_command)
        
connection.commit()
csvfile.close()

#create gene table
sql_command = """
DROP TABLE IF EXISTS gene;
"""

cursor.execute(sql_command)

sql_command = """
CREATE TABLE IF NOT EXISTS gene (
   entrez_id INTEGER PRIMARY KEY, 
gene_symbol VARCHAR(10),
gene_name VARCHAR(30));"""

cursor.execute(sql_command)

#import patient info from patients.csv
with open('entrez_ids_genesymbol.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        sql_command = """INSERT INTO gene (entrez_id, gene_symbol, gene_name) 
        VALUES ({entrez_id}, "{gene_symbol}", "{gene_name}");""".format(
            entrez_id = row[0],
            gene_symbol = row[1],
            gene_name = row[2]
        )
        cursor.execute(sql_command)
        
connection.commit()
csvfile.close()

# 0: exit
# 3: get gene info
# 4: get patient info

info = """
# 0: exit
# 3: get gene info
# 4: get patient info
"""
print info
command = input("Enter your command: ")
if (command == 3) :
        input_entrez_id = raw_input("Enter gene ID: ")
        sql_command = """SELECT * FROM gene WHERE entrez_id ="{entrez_id}";""".format(
            entrez_id = input_entrez_id )
        cursor.execute(sql_command)


        ans = cursor.fetchone()
        print("\n")
        print("Gene ID: " + str(ans[0]))
        print("Gene Symbol: " + ans[1])
        print("Gene Name: " + ans[2])
        print("\n")
        
        

elif (command == 4) :

        #getPatientInfo():
        input_patient_ID = raw_input("Enter patient ID: ")
        sql_command = """SELECT * FROM patient WHERE patient_ID ="{patient_ID}";""".format(
            patient_ID = input_patient_ID )
        cursor.execute(sql_command)


        ans = cursor.fetchone()
        print("\n")
        print("Patient ID: " + ans[0])
        print("Age: " + str(ans[1]))
        print("Gender: " + ans[2])
        print("Education: " + ans[3])
        print("\n")
        
        


connection.close();
