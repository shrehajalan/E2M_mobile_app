from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
URL_DATABASE = "mysql+pymysql://root:password123@localhost:3306/client_registration"
URL_DATABASE2 = "mysql+pymysql://root:password123@localhost:3306/shop_management_db"
#import logging
#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

engine = create_engine(URL_DATABASE)#echo = True
#creates a sessionmaker factory object
sessionLocal = sessionmaker(autocommit = False, autoflush= False,bind = engine)
Base = declarative_base()

engine2 = create_engine(URL_DATABASE2,echo = True)#echo = True
sessionLocal2 = sessionmaker(autocommit = False, autoflush= False,bind = engine2)
Base2 = declarative_base()

