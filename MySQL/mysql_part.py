from credentials_file.credentials_location import My_SQL_credentials as CREDS   # imports dictionary of MySQL credentials and info (database, table)
from mysql.connector import connect, Error


# creates the query and connects to the mysql database before inserting data dictionary as data into the table  
def insert_into_MySQL(data: dict):
    
    query = f"INSERT INTO {CREDS['table']} ({', '.join(data)}) VALUES ({('%s, '*len(data)).rstrip(', ')})"
    args = [*data.values()]
    
    try:
        with connect(
            host = CREDS['host'],
            user = CREDS['user'],
            password = CREDS['password'],
            database = CREDS['database']
        ) as connection:

            cursor = connection.cursor()
            cursor.execute(query, args)
            
            connection.commit()

    except Error as e:
        print(e)
