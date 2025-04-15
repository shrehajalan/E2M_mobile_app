#To run a FastAPI application file, you need a web server to 
# handle HTTP requests and execute your FastAPI app. The most 
# common server used with FastAPI is Uvicorn. Here's how you can run your FastAPI application:

#The Python interpreter is the program that runs Python code
#When running a FastAPI application (or any Python app), 
# the interpreter is responsible for executing the Python code
#  and managing dependencies (like FastAPI and Uvicorn).


#If you've already set the interpreter in Visual Studio Code
#to the one defined in your virtual environment, you can run:directly 
#from your terminal (without explicitly activating the virtual environment in the terminal). 

#The client is any system, device, or application that sends HTTP requests
#  to the server to interact with the API like google chrome,IE,postman.
#A "server" is like a computer that runs 24/7. It listens for requests 
#You Start the Server: By running a command like:uvicorn main:app --reload
#Uvicorn Loads FastAPI and starts listening for requests on the specified address and port.
#When you start the server, it "loads" your FastAPI application into memory. The server delegates
#incoming requests to the FastAPI app, which processes them and sends responses back.
#The server (Uvicorn) is like a telephone operator. It handles all the "calls" (requests) and 
# directs them to the right person (your FastAPI app).
#The FastAPI app is like the person receiving the calls. It knows how to respond to specific queries 
#and provides the needed information.


import json
import fastapi
#from celery import Celery
#from celery.schedules import crontab
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException,Depends,status
from pydantic import BaseModel
import models
from models import HistorySellModel,HistoryHandBillModel,HistorySellCashCustomerModel,HistoryPurchaseModel,EmployeeRegistrationModel,EmployeeJobDetailsModel
from models import EmployeeSalaryPaymentModel, EmployeeExtraPaymentModel
from database import engine,sessionLocal,client_db,resource_db
from sqlalchemy.orm import Session
from schema_data import ClientRegistration,ClientLogin,ClientDataDashboard,ClientDataSearchQuery,ClientDataSearchQueryOnItem,ClientDataInvoiceDetail,ClientDataStockDetail,SetEmpPasswordDetails
from schema_data import EmployeeListFromName,EmployeeSalaryEntryDetail,EmployeeExtraPaymentDetail,EmployeeAttendanceDetail
from schema_data import ExpenseDetail
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from models import ClientRegistrationModel,ProductListModel
from stockLogic import brand_list_stock_query, item_list_stock_query,total_stock_query
from checking import loginverification,mobileVerification,generate_unique_client_code
from employeeLogic import generate_unique_employee_code,check_employee_registration,check_new_employee_mob,check_unique_values,emp_login_verification,extract_client_code,emp_record_verification,emp_generate_otp,emp_otp_check,emp_password_change
from employeeLogic import emp_name_list,emp_salary_entry,emp_extra_payment_entry,expense_entry,emp_mark_attendance,emp_estimated_salary
from dashboardLogic import MaxclientId,dashboardSale,dashboardPurchase
from sqlalchemy import func
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt, ExpiredSignatureError
from datetime import datetime, timedelta
from searchLogic import search_query_date_func,search_query_invoice_func,search_query_party_func,party_list_search_query,search_query_brand_func,tool_brand_list_search_query
from itemSerachLogic import item_search_query_date_func,item_search_query_item_party_func,item_search_query_item_func
from itemSerachLogic import itemName_list_search_query,sellerParty_list_search_query
from schema_data import EmployeeRegistration, EmployeeLogin
#import auto_process
#from auto_process import process_carry_forward_leaves

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

app = FastAPI()
#process_carry_forward_leaves.delay()

#models.Base is typically an instance of declarative_base() acts as the foundation for all your ORM (Object-Relational Mapping) models.
#The create_all() method inspects this metadata and creates the tables in the database if they don’t already exist.
#When you pass bind=engine, SQLAlchemy knows where (which database) to create the tables.
# Ensure tables are created
#It directly interacts with the database engine and sends create table sql commands
#A session is used for querying , inserting,updating. deleting data, but not with for schema

#OAuth2PasswordBearer is a class provided by FastAPI.It automatically 
# looks for a token in the Authorization header of incoming HTTP requests.
# By default, it expects the token to be in the Authorization header with the format Bearer <token>.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#The function creates a database session, provides it to the caller using yield,
#and ensures that the session is properly closed after use, even if an exception occurs.
#using sessionmaker factyory object it creates session object,is the ORM layer that sits 
#on top of the engine, providing a higher-level interface..The session allows you to use 
#Python objects and methods instead of writing raw SQL.

def get_db():
    db = sessionLocal()
    try:
        return db
    finally: 
        db.close()
    
def get_db2(clientId : str):
    engine2, sessionLocal2 = client_db(clientId)
    models.Base2.metadata.create_all(bind=engine2)
    db2 = sessionLocal2()
    try:
        return db2
    finally: 
        db2.close()

def get_db3(clientId : str):
    engine3, sessionLocal3 = resource_db(clientId)
    models.Base3.metadata.create_all(bind=engine3)

    db3 = sessionLocal3()
    try:
        return db3
    finally: 
        db3.close()

app.mount("/static", StaticFiles(directory="static"), name="static")

def hash_password(password: str):
    return pwd_context.hash(password)

def get_current_employee(token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        mobilenumber = payload.get("sub")
        role = payload.get("role")
        clientId = payload.get("clientId")
        empId = payload.get("empId")

        if mobilenumber is None or role is None:
            return{
                    "status" : 0,
                    "message":"Could not validate credentials",
                    "clientId" : "",
                    "empId" : "",
                    "mobilenumber":"",
                    "role":""
                  }
        db3 = get_db3(clientId)
        employee = db3.query(EmployeeRegistrationModel).filter(EmployeeRegistrationModel.mobileNum == mobilenumber).first()
        if not employee:
            return{
                    "status" : 0,
                    "message":"Could not validate credentials",
                    "clientId" : "",
                    "empId" : "",
                    "mobilenumber":"",
                    "role":""
                  }
        else:
            return {
                    "status" : 1,
                    "message":"credentials validated successfully",
                    "clientId" : clientId,
                    "empId" : empId,
                    "mobilenumber": mobilenumber,
                    "role": role
                    }
    except ExpiredSignatureError:
          return{
                    "status" : 0,
                    "message" : "Token has expired",
                    "clientId" : "",
                    "empId" : "",
                    "mobilenumber":"",
                    "role":""
              }
    except JWTError as e:
        return{
                    "status" : 0,
                    "message":f"Invalid token: {e}",
                    "clientId" : "",
                    "empId" : "",
                    "mobilenumber":"",
                    "role":""
              }

#function will decode the token, extract the user's role
def get_current_user(token:str = Depends(oauth2_scheme), db : Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        mobilenumber = payload.get("sub")
        role = payload.get("role")
        clientId = payload.get("clientId")
        print("mobilenumber",mobilenumber)

        if mobilenumber is None or role is None:
            print("mobilenumber")
            return{
                    "status" : 0,
                    "message":"Could not validate credentials",
                    "clientId" : "",
                    "mobilenumber":"",
                    "role":""
                  }
        
        client = db.query(ClientRegistrationModel).filter(ClientRegistrationModel.mobileNumber == mobilenumber).first()
       
        if not client:
            return{
                    "status" : 0,
                    "message":"Could not validate credentials",
                    "clientId" : "",
                    "mobilenumber":"",
                    "role":""
                  }
        else:
            return {
                    "status" : 1,
                    "message":"credentials validated successfully",
                    "clientId" : clientId,
                    "mobilenumber": mobilenumber,
                    "role": role
                    }
    except ExpiredSignatureError:
          return{
                    "status" : 0,
                    "message" : "Token has expired",
                    "clientId" : "",
                    "mobilenumber":"",
                    "role":""
              }
    except JWTError as e:
        return{
                    "status" : 0,
                    "message":f"Invalid token: {e}",
                    "clientId" : "",
                    "mobilenumber":"",
                    "role":""
              }

#check if the user is an admin:
def require_admin(user : dict = Depends(get_current_user)):
    if user['role']=="":
        return user
    if user['role']!="admin":
        user['status'] = 0
        user['message'] = "Admin privileges required"
        return user
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def dashboard_display_admin(db2 : Session):
    saleDic = await dashboardSale(db2)
    if saleDic["status"]==0:
        saleDic['curr_day_num'] = "",
        saleDic['curr_week_num'] = "",
        saleDic["current_month"] ="",
        saleDic["current_quarter"] ="",
        saleDic["current_year"] ="",
        saleDic["sale"] = None,
        saleDic["purchase"] =None,
        saleDic["top_products_by_cash"] =[],
        saleDic["top_products_by_credit"] =[]
        return saleDic
    
    purchaseDic = await dashboardPurchase(db2)
    if purchaseDic["status"]==0:

        saleDic['curr_day_num'] = "",
        saleDic['curr_week_num'] = "",
        purchaseDic["current_month"] ="",
        purchaseDic["current_quarter"] ="",
        purchaseDic["current_year"] ="",
        purchaseDic["sale"] = None,
        purchaseDic["purchase"] =None,
        purchaseDic["top_products_by_cash"] =[],
        purchaseDic["top_products_by_credit"] =[]
        return purchaseDic

    response = {
        "status" : "1",
        "message" : "Successfully calculated",

        "sale" : {"curr_day_num" : saleDic['curr_day_num'],"curr_week_num" : saleDic['curr_week_num'],
                  "current_month " : saleDic['name'][0],"current_quarter " : saleDic['name'][1],
                "current_year " : saleDic['name'][2],
                "monthly":saleDic['value'][0],"quarterly":saleDic['value'][1],"yearly":saleDic['value'][2],
                "curr_month_day_values":saleDic['graph'][0],"curr_quarter_week_values":saleDic['graph'][1],
                "curr_year_month_values":saleDic['graph'][2]},

        "purchase" : {"curr_day_num" : saleDic['curr_day_num'],"curr_week_num" : saleDic['curr_week_num'],
                      "current_month " : saleDic['name'][0],"current_quarter " : saleDic['name'][1],
                    "current_year " : saleDic['name'][2],
                    "monthly":purchaseDic['value'][0],"quarterly":purchaseDic['value'][1],
                    "yearly":purchaseDic['value'][2],"curr_month_day_values":purchaseDic['graph'][0],
                    "curr_quarter_week_values":purchaseDic['graph'][1],"curr_year_month_values":purchaseDic['graph'][2]},
        "top_products_by_cash" : saleDic['top_products_by_cash'],
        "top_products_by_credit" : saleDic['top_products_by_credit']
        }
    return(response)
  
async def dashboard_display_nonadmin(db2 : Session):
    print("NOT YET IMPLEMENTED CODE")
    return{   "status" : 0,
              "message":"NOT YET IMPLEMENTED CODE"
          }
    
@app.get("/", response_class=FileResponse)
def loginPage():
    return FileResponse("static/login.html")

@app.post("/login")
async def login_for_access_token(form_data : ClientLogin,db:Session = Depends(get_db)):
    form_data = form_data.dict()
    mobileNumber=str(form_data['mobileNumber'])
    password=form_data['password']
    verificationStatus = await loginverification(mobileNumber, password,db, pwd_context)
    if verificationStatus['status'] == 0:
        verificationStatus['access_token']=""
        verificationStatus["token_type"]=""
        return verificationStatus
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": verificationStatus['db_user'].mobileNumber, "role": verificationStatus['db_user'].role, "clientId" : verificationStatus['db_user'].clientId}, expires_delta=access_token_expires)
    return {"status":"1", "message":"login successfully","isCustomer":verificationStatus['isCustomer'],"clientId":verificationStatus['db_user'].clientId ,"access_token": access_token, "token_type": "bearer"}

@app.post("/registerSubmit",status_code=status.HTTP_201_CREATED)
async def user_post(post : ClientRegistration,db:Session = Depends(get_db)):
    post = post.dict()
    mobileNumber = post['mobileNumber']
    result= await mobileVerification( mobileNumber,db)
    if result['status'] == 0:
        jsonRegistrationstatus=result
    else:
        try:
            clientId_dic=await MaxclientId(db)
            if clientId_dic['status'] == 0:
                return clientId_dic
            else:
                clientId = clientId_dic['id']
            clientId=clientId+1
            status=0

            post['clientId']=clientId
            post['status']=status
            post['role']='nonadmin'
            post['password'] = hash_password(post['password'])
            post['uniqueCode'] = await generate_unique_client_code(db)
            print("Uc",post['uniqueCode'])
            print("password",post['password'])

            db_user =ClientRegistrationModel(**post)
            db.add(db_user) 
            db.commit()
            db.refresh(db_user)
            jsonRegistrationstatus={"status":1,"message":"Resgistration done successfully"}
        except Exception as e:
            jsonRegistrationstatus = {"status":"0", "message":f" Error: {e}"}
    return jsonRegistrationstatus

@app.post("/dashboard")
async def dashboard_display(post : ClientDataDashboard,user : dict = Depends(require_admin)):
    if user['status'] == 0 :
        return user
    
    db2 = get_db2(post.clientId)
    if user['role'] == "admin" :
        return await dashboard_display_admin(db2)
    else :
        return await dashboard_display_nonadmin(db2)
    db2.close()

@app.post("/searchQuery")
async def search_query_invoice(post:ClientDataSearchQuery,user : dict = Depends(require_admin)):  
    if user['status'] == 0:
        return user
    if user['role'] != "admin" :
        return user
    
    db2 = get_db2(post.clientId)
    post_dic= post.dict()
    sType = post_dic['sType']
    typeFilter  =  post_dic["typeFilter"]
    flag = int(post_dic['flag'])
     
    if flag == 0 and typeFilter == "party":
        return(await party_list_search_query(post,db2))
     
    if flag == 0 and typeFilter == "brand":
        return(await tool_brand_list_search_query(post,db2))
    
    elif(flag == 1):
        if typeFilter == "invoice":
            return(await search_query_invoice_func(post,db2))
        elif typeFilter == "party":
            return(await search_query_party_func(post,db2))
        elif typeFilter == "date":
            return(await search_query_date_func(post,db2))
        elif typeFilter == "brand":
            return(await search_query_brand_func(post,db2))
    db2.close()
    
@app.post("/itemSearchQuery")
async def item_based_search_query_invoice(post:ClientDataSearchQueryOnItem,user : dict = Depends(require_admin)):
    if user['status'] == 0:
        return user
    if user['role'] != "admin" :
        return user
    db2 = get_db2(post.clientId)
    post_dic= post.dict()
    typeFilter  =  post_dic["typeFilter"]
    typeFilter2  =  post_dic["typeFilter2"]
    flag = int(post_dic['flag'])

    if flag == 0:
        if typeFilter == "itemName" and typeFilter2 == "" :
            return(await itemName_list_search_query(post,db2))
        if typeFilter == "" and typeFilter2 == "partyName" :
            return(await sellerParty_list_search_query(post,db2))
        
    if flag == 1 :
        if typeFilter == "itemName" and typeFilter2 == "":
            return(await item_search_query_item_func(post,db2))
        elif typeFilter == "date" and typeFilter2 == "":
            return(await item_search_query_date_func(post,db2))
        elif typeFilter == "itemName" and typeFilter2 == "partyName":
            return(await item_search_query_item_party_func(post,db2))
    db2.close()

@app.post("/invoiceDetail")
async def search_query_invoice_details(post:ClientDataInvoiceDetail,user : dict = Depends(require_admin)):
    if user['status'] == 0:
        return user
    if user['role'] != "admin" :
        return user
    
    db2 = get_db2(post.clientId)
    post_dic= post.dict()
    invoice  =  post_dic["invoice"]
    type =  post_dic["type"]

    if type == "sale": 

        records = db2.query(HistorySellModel).filter(HistorySellModel.invoiceNo == invoice).all()
        
        if not records:  # If no records found, search in HistorySellCashCustomerModel
            records = db2.query(HistorySellCashCustomerModel).filter(HistorySellCashCustomerModel.chalanNo == invoice).all()

        if not records:  # If still no records found, search in HistoryHandBillModel
            records = db2.query(HistoryHandBillModel).filter(HistoryHandBillModel.invoiceNo== invoice).all()
        print("records",len(records))
        return records if records else None
    
    if type == "purchase": 
        
        records = db2.query(HistoryPurchaseModel).filter(HistoryPurchaseModel.invoiceNo== invoice).all()
        print("records",len(records))
        
        return records if records else None
    db2.close()

@app.post("/stockDetail")
async def calculate_stock_detail(post:ClientDataStockDetail, user:dict = Depends(require_admin)):
    if user['status'] == 0:
        return user
    if user['role'] != "admin" :
        return user
    
    db2 = get_db2(post.clientId)
    post = post.dict()
    type = post['type']
    flag = int(post['flag'])

    if flag == 0 and type == "itemName":
        return(await item_list_stock_query(post,db2))
    if flag == 0 and type == "brand":
        return(await brand_list_stock_query(post,db2))
    if flag == 1 :
        return(await total_stock_query(post,db2))
    db2.close() 

@app.post("/employeeRegistration")
async def employee_registration(post:EmployeeRegistration, user:dict = Depends(require_admin), db:Session = Depends(get_db)):
    try:
        if user['status'] == 0:
            return user
        if user['role'] != "admin" :
            return user
        db3 = get_db3(post.clientId)
        post = post.dict()
        post1 = {}
        post1['name'] = post['name']
        post1['dateOfBirth'] =  datetime.strptime(post['dateOfBirth'], "%d-%m-%Y").date()
        post1['gender'] = post['gender']
        post1['mobileNum'] = post['mobileNum']
        post1['mailId'] = post['mailId']
        post1['address'] = post['address']
        post1['zip'] = post['zip']
        post1['state'] = post['state']
        post1['proofType'] = post['proofType']
        post1['proofNumber']  = post['proofNumber']
        post1['photo'] = post['photo']
        post1['bankName'] = post['bankName']
        post1['accountNumber'] = post['accountNumber']
        post1['ifscCode'] = post['ifscCode']
        post1['upiId'] = post['upiId']
        post1['password']="employee"


        uniqueCode = await generate_unique_employee_code(post['clientId'],post1['mobileNum'],db,db3)
        if uniqueCode == None:
            return{"status":0,"message":"No such client to register its employee detail"}
        
        post2 = {}
        post2['designation'] = post['designation'] 
        post2['department'] = post['department'] 
        post2['joinDate'] =  datetime.strptime(post['joinDate'], "%d-%m-%Y").date() 
        post2['salary'] = float(post['salary']) 

        latitude = post['empReportingLatitude']
        longitude = post['empReportingLongitude']


        res=await check_new_employee_mob(post1['mobileNum'],db3)
        if res['status'] == 1:
            return{"status":0, "message":"already registered with this mobile number"}
        res=await check_unique_values(post1['accountNumber'], post1['proofNumber'], post1['upiId'], post1['mailId'], db3)
        if res['status'] == 1:
            return{"status":0, "message":"Record with same unique details already exists!Check with accountNumber/proofNumber/upiId/mailId..It has to be unique"}

        
        result = await check_employee_registration(latitude, longitude, post1, post2, db3)
        res=await check_new_employee_mob(post1['mobileNum'],db3)
        empid=str(res['empId'][0])
        empid=str(uniqueCode)+str(empid)
        result['message']=result['message'] + f" with loginid : {empid}"
        db3.close()
        return(result)
    except Exception as e:
        return ({'status':0,"message":e})

@app.post("/employeeLogin")
async def employee_login(post:EmployeeLogin, db:Session = Depends(get_db)):
    post = post.dict()
    empId = post['empId']
    password = post['password']
    result = await extract_client_code(empId, db)
    if result['status'] == 0:
        return result
    else:
        db3 = get_db3(result['clientId'])
        verificationStatus = await emp_login_verification(post,db3)
        if verificationStatus['status'] == 0:
            verificationStatus['empId'] = ""
            verificationStatus['access_token']= ""
            verificationStatus["token_type"]= ""
            return verificationStatus
        else:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(data={"sub": verificationStatus['data'].mobileNum, "role": verificationStatus['data'].role, "empId" : verificationStatus['data'].employeeId, "clientId" : result['clientId']}, expires_delta=access_token_expires)
            return {"status":"1", "message":"login successfully","clientId" : result['clientId'],"employeeNum" : verificationStatus['data'].employeeId,"access_token": access_token, "token_type": "bearer"}

@app.post("/empForgetPassword")
async def emp_forget_password(post:SetEmpPasswordDetails, db:Session = Depends(get_db)):
    post = post.dict()
    flag = int(post['flag'])

    if flag == 0:
        if post['empId'] == "":
             return({'status':0,'message':"please enter employeeID",'clientId':post['clientId'], "employeeNum":post['employeeNum']})
        result = await extract_client_code(post['empId'], db)
        if result['status'] == 0:
            return({'status':0,'message':"entered wrong empid",'clientId':"", "employeeNum":""})
        else:
            db3 = get_db3(result['clientId'])
            empRecordStatus = await emp_record_verification(post['empId'], db3)
            if empRecordStatus['status'] == 0:
                return empRecordStatus
            otpRecord = await emp_generate_otp(empRecordStatus['employeeNum'], db3)
            if otpRecord['status'] == 1:
                otpRecord['clientId'] = result['clientId']
            return(otpRecord)

    elif flag == 1:
         if post['otp'] == "":
             return({'status':0,'message':"please enter otp",'clientId':post['clientId'], "employeeNum":post['employeeNum']})
         db3 = get_db3(post['clientId'])
         otpMatchResult = await emp_otp_check(post['employeeNum'],post['otp'], db3)
         otpMatchResult['clientId'] = post['clientId']
         return(otpMatchResult)
    
    elif flag == 2:
        if post['newPassword'] == "":
             return({'status':0,'message':"please enter password",'clientId':post['clientId'], "employeeNum":post['employeeNum']})
        db3 = get_db3(post['clientId'])
        passwordChange = await emp_password_change(post['employeeNum'],post['newPassword'],db3)
        passwordChange['clientid'] = post['clientId']
        return(passwordChange)

@app.post("/empNameList")
async def fetch_emp_name_list(post:EmployeeListFromName, user:dict = Depends(require_admin)):
    if user['status'] == 0:
        return user
    if user['role'] != "admin" :
        return user
    
    db3 = get_db3(post.clientId)
    empList = await emp_name_list(post.dict(),db3)
    return empList

@app.post("/empSalaryEntry")
async def emp_salary_entry_func(post:EmployeeSalaryEntryDetail, user:dict = Depends(require_admin)):
    try:
        if user['status'] == 0:
            return user
        if user['role'] != "admin" :
            return user
        
        post =  post.dict()
        db3 = get_db3(post['clientId'])
        
        emp_record = db3.query(EmployeeRegistrationModel).filter(EmployeeRegistrationModel.employeeId == post['employeeNum']).first()
        if not emp_record:
            raise ValueError(f"Employee with employee_number as {post['employeeNum']} is not registered")
        result = await emp_salary_entry(post, db3)
        return(result)
    
    except ValueError as ve:
        status = {"status": 0, "message": str(ve)}
        return(status)
    except Exception as e:
        status = {"status": 0, "message": f"Error: {e}"}
        return(status)

@app.post("/empExtraPaymentEntry")
async def emp_extra_payment_entry_func(post:EmployeeExtraPaymentDetail, user:dict = Depends(require_admin)):
    try:
        if user['status'] == 0:
            return user
        if user['role'] != "admin" :
            return user
        
        db3 = get_db3(post.clientId)
        post =  post.dict()
        emp_record = db3.query(EmployeeExtraPaymentModel).filter(EmployeeExtraPaymentModel.employeeId == post['employeeNum']).first()
        if not emp_record:
            raise ValueError(f"Employee with employee_number as {post['employeeNum']} is not registered")
        result = await emp_extra_payment_entry(post,db3)
        return(result)
  
    except ValueError as ve:
        status = {"status": 0, "message": str(ve)}
    except Exception as e:
        status = {"status": 0, "message": f"Error: {e}"}
    return(status)

@app.post("/expenseEntry")
async def expense_entry_func(post:ExpenseDetail, user:dict = Depends(require_admin)):
    if user['status'] == 0:
        return user
    if user['role'] != "admin" :
        return user
    
    db3 = get_db3(post.clientId)
    post =  post.dict()
    result = await expense_entry(post,db3)
    return(result)

@app.post("/employeeMarkAttendance")
async def employee_mark_attendance_func(post:EmployeeAttendanceDetail,user:dict = Depends(get_current_employee)):
    if user['status'] == 0:
        return user
    clientId = post.clientId
    date = post.attendanceDate
    if date != date.today():
        return{'status' : 0, 
               'message' : "Attendance can only be be taken for current date and not previous date.",
               "clientId" : "",
               "empId" : "",
               "mobilenumber":"",
               "role":""}
    db = get_db()
    record = db.query(ClientRegistrationModel).filter(ClientRegistrationModel.clientId == clientId).first()
    if not record:
            return{
                    "status" : 0,
                    "message":"Client ID is not valid.No client with this ID is registered.",
                    "clientId" : "",
                    "empId" : "",
                    "mobilenumber":"",
                    "role":""
                  }

    db3 = get_db3(post.clientId)
    post = post.dict()
    attendance_status = await emp_mark_attendance(post, db3)
    return(attendance_status)

    















    
    
    



