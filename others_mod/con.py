import mysql.connector
from mysql.connector import pooling
import os


dbconfig = {
    "host": os.environ.get("DB_HOST"),
    "port": os.environ.get("DB_PORT"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "database": "test", # TiDB creates a 'test' database by default
    "ssl_ca": "/etc/ssl/certs/ca-certificates.crt" # Required for TiDB security
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
    