import pyodbc

class person:
    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name

conn = pyodbc.connect('DRIVER={FreeTDS};Server=169.254.208.1;PORT=64909;DATABASE=DemoDB2;UID=master;PWD=control;TDS_Version=7.2;')
cursor = conn.cursor()
last_name = "ivie"
cursor.execute(f"dbo.spPerson_ReadAll")
people = list()
for row in cursor.fetchall():
    print (row)
    people.append(person(row[0], row[1], row[2]))


print(people[2].last_name)
print(len(people))
    