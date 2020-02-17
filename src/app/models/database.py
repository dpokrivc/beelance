import mysql.connector
from dotenv import load_dotenv
import os

groupid = os.getenv("groupid").lstrip("0")

"""
Connect the webserver to the database using the python mysql connecter. 
Change the host address depending on where the mysql server is running. To connect to the 
preconfigured docker container address use the Docker address. The default port is 3306.
"""
db = mysql.connector.connect(
    user='root', 
    password='root',
    host='10.' + groupid + '.0.5',   # Docker address
    #host='0.0.0.0',    # Local address
    database='db'
)
    
