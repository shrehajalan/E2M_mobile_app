from models import ClientRegistrationModel,HistorySellModel,HistoryPurchaseModel
from fastapi import  HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import func, extract
import calendar
import re


def verify_password(plain_password, hashed_password,pwd_context):
    print(plain_password)
    print(hashed_password,pwd_context)
    return pwd_context.verify(plain_password, hashed_password)

async def loginverification(mobileNumber:str,password:str,db:Session,pwd_context):
    try:
        if len(mobileNumber) != 10:
            return {"status": 0,"message":"mobile number donnot conatin 10 digits"}
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
        print("MB:",mobileNumber)
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
        
    
async def displayAmount_check(type_sale_purchase : str,time_period : str, db : Session):
    current_year = datetime.now().year
    current_month = datetime.now().month
   
    if time_period == 'monthly':
        start_month = current_month
        print(start_month)
        end_month = current_month

    elif time_period == 'quarterly':
        quarter = int((current_month-1)/3) + 1
        end_month = quarter * 3
        start_month = (end_month - 3)+ 1
       

    elif time_period == 'semiannual':
        semiannual = int((current_month-1)/6)+1
        end_month = semiannual * 6
        start_month = (end_month - 6)+1

    else:
        end_month = 12
        start_month = 1
    print("jjjjj")
    start_date = datetime(current_year, start_month, 1)
    _,num_days = calendar.monthrange(current_year, end_month)
    end_date = datetime(current_year, end_month, num_days)

    try:
        if type_sale_purchase == 'sell':
            table = HistorySellModel
        elif type_sale_purchase == 'purchase':
            table = HistoryPurchaseModel
        result =  db.query(
                        func.sum(table.qty).label('total_qty'),
                        func.sum(table.Total_price).label('total_price')).filter(
                             table.Date_bill >= start_date,
                             table.Date_bill <= end_date).first()
        db.commit()

        month_list = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sept","Oct","Nov","Dec"]
        time = month_list[start_month-1]+"-"+month_list[end_month-1]+" "+str(current_year)
        print("helloend")
        if not result:
            return {
                    "status" : 0,
                    'message' :'No records to calculate with',
                    'action' : 'null',
                    'data':{
                        "time_period":time,
                        "total_qty": 0,
                        "total_price": 0}
                    }
        else:
            return {"status" : 1,
                    'message' :'Successfully calculated',
                    'action' : 'null',
                    'data':{
                        "time_period":time,
                        "total_qty": result.total_qty,
                        "total_price": result.total_price}
                    }
    except Exception as e: 
        raise HTTPException(status_code=500, detail=e)

    

