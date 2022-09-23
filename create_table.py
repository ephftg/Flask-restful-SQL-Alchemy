# code to learn how sqlite interact with python code
import sqlite3 # allow creation of database and then to query it 
# sqlite3 is light in that it requires only a database file, so write data to database slower

# initialize a connection with the data base of interest, create data.db if data base does not exists
connection = sqlite3.connect('data.db')

# create cursor related to the connection, cursor is a virtual cursor to help select and run the query and store the result
cursor = connection.cursor()

# CREATE A TABLE in sqlite database using the sqlite3 command line in string
# create table with table name users, with the following column names and data type for each column
# id should increase as number increases
# INTEGER PRIMARY KEY  --> automatic increase by 1 each time for id for new user added
create_table_query = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table_query) # use cursor to run query line to create table 
# for input, don't need input id since id will be assign automatically 

# CREATE DATA BASE FOR ITEMS, AND ADD IN TEST ITEM TO TRY OUT CODE 

create_itemtable_query = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_itemtable_query)

#cursor.execute("INSERT INTO items VALUES ('test', 13.45)")

connection.commit()
connection.close()