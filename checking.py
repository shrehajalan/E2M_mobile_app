from models import ClientRegistrationModel,HistorySellModel,HistoryPurchaseModel
from fastapi import  HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import func, extract
import calendar
import re
import random
import string

async def generate_unique_client_code(db: Session):
    while True:
        random_code = ''.join(random.choices(string.ascii_uppercase, k=4))
        existing_code = db.query(ClientRegistrationModel).filter_by(uniqueCode=random_code).first()

        if not existing_code:
            return random_code
        
def verify_password(plain_password, hashed_password,pwd_context):
    print(plain_password)
    print(hashed_password,pwd_context)
    return pwd_context.verify(plain_password, hashed_password)

async def loginverification(mobileNumber:str,password:str,db:Session,pwd_context):
    try:
        if len(mobileNumber) != 10:
            return {"status": 0,"message":"mobile number donnot conatin 10 digits","isCustomer":""}
        if not(re.fullmatch(r'\d{10}', mobileNumber)):
            return {"status": 0,"message":"mobile number not entered in digits","isCustomer":""}
        db_user = db.query(ClientRegistrationModel).filter( ClientRegistrationModel.mobileNumber == mobileNumber).first()
        if db_user:
            customer=db_user.status
            if verify_password(password, db_user.password,pwd_context):
                return {"status": 1,"message":"verifiedSuccessfully","isCustomer":customer,"db_user":db_user}
            else:
                return {"status": 0,"message":"wrongPassword","isCustomer":customer}
        else:
            return {"status": 0,"message":"notRegistered","isCustomer":0}
    except Exception as e:
        return {"status": 0,"message":f"Error: {e}","isCustomer":""}
    
async def mobileVerification(mobileNumber:str,db:Session):
    try:
        if len(mobileNumber) != 10:
            return {"status": 0,"message":"mobile number donnot conatin 10 digits"}
        if not(re.fullmatch(r'\d{10}', mobileNumber)):
            print("2")
            return {"status": 0,"message":"mobile number not entered in digits"}
        db_user = db.query(ClientRegistrationModel).filter( ClientRegistrationModel.mobileNumber == mobileNumber).first()
        if db_user:
            return {"status": 0,"message":"already registered with the given mobile number"}
        else:
            return {"status": 1}
    except Exception as e:
        return {"status": 0,"message":f"Error: {e}"}