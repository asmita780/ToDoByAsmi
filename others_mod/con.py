import mysql.connector
from mysql.connector import pooling

dbconfig = {  
    "host":"localhost",
    "user":"root",
    "password":"root",
    "database":"mytododb"
}

connection_pool = pooling.MySQLConnectionPool( #creating pool
    pool_name = "mypool",
    pool_size = 5,
    **dbconfig
)

def get_connection(): #normal function
    try:

        return connection_pool.get_connection() # returning connection get_connection is predefined method to get connection from pool
    
    except mysql.connector.Error as err:

        return None
    