from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pymysql

URL_DATABASE = "mysql+pymysql://root:password123@localhost:3306/client_registration"

engine = create_engine(URL_DATABASE)#echo = True
sessionLocal = sessionmaker(autocommit = False, autoflush= False,bind = engine)#creates a sessionmaker factory object

def client_db(clientId:str):
    database_name = f"shop_management_db_{clientId}"

    # Use raw MySQL connection to ensure database creation works
    try:
        connection = pymysql.connect(host='localhost', user='root', password='password123')
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        connection.commit()  # Explicit commit for safety
        cursor.close()
        connection.close()
        print(f"Database '{database_name}' created successfully.")
    except Exception as e:
        print(f"Error while creating database: {e}")
        return None, None
    
    URL_DATABASE2 = f"mysql+pymysql://root:password123@localhost:3306/shop_management_db_{clientId}"
    engine2 = create_engine(URL_DATABASE2)#echo = True
    sessionLocal2 = sessionmaker(autocommit = False, autoflush= False,bind = engine2)
    return engine2,sessionLocal2
    
def resource_db(clientId: str):  
    database_name = f"resource_db_{clientId}"

    # Use raw MySQL connection to ensure database creation works
    try:
        connection = pymysql.connect(host='localhost', user='root', password='password123')
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        connection.commit()  # Explicit commit for safety
        cursor.close()
        connection.close()
    except Exception as e : 
        return None, None

    # Now connect to the newly created database using SQLAlchemy
    URL_DATABASE3 = f"mysql+pymysql://root:password123@localhost:3306/{database_name}"
    engine3 = create_engine(URL_DATABASE3)
    sessionLocal3 = sessionmaker(autocommit=False, autoflush=False, bind=engine3)
    return engine3, sessionLocal3


