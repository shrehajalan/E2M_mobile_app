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
from fastapi import FastAPI, HTTPException,Depends,status
from pydantic import BaseModel
import models
from database import engine, sessionLocal,sessionLocal2,engine2
from sqlalchemy.orm import Session
from schema_data import ClientRegistration,ClientLogin,AmountCalc,ClientDataDashboard,ClientDataSearchQuery
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from models import ClientRegistrationModel
from checking import loginverification,mobileVerification,displayAmount_check
import logging
from queryLogic import MaxclientId,dashboardSale,dashboardPurchase
import passlib
import bcrypt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt, ExpiredSignatureError
from datetime import datetime, timedelta
from searchLogic import search_query_date_func,search_query_invoice_func,search_query_party_func,party_list_search_query

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 100

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
#models.Base is typically an instance of declarative_base() acts as the foundation for all your ORM (Object-Relational Mapping) models.
#The metadata attribute of Base contains the information about all the models and their associated tables.
#The create_all() method inspects this metadata and creates the tables in the database if they don’t already exist.
#When you pass bind=engine, SQLAlchemy knows where (which database) to create the tables.
models.Base2.metadata.create_all(bind=engine2)

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
        yield db
    finally: 
        db.close()

def get_db2():
    db2 = sessionLocal2()
    try:
        yield db2
    finally: 
        db2.close()

app.mount("/static", StaticFiles(directory="static"), name="static")

def hash_password(password: str):
    return pwd_context.hash(password)

#function will decode the token, extract the user's role
def get_current_user(token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        mobilenumber = payload.get("sub")
        role = payload.get("role")

        if mobilenumber is None or role is None:
            return{
                    "status" : 0,
                    "message":"Could not validate credentials",
                    "mobilenumber":"",
                    "role":""
                  }
        return {
                    "status" : 1,
                    "message":"credentials validated successfully",
                    "mobilenumber": mobilenumber,
                    "role": role
               }
    except ExpiredSignatureError:
          return{
                    "status" : 0,
                    "message" : "Token has expired",
                    "mobilenumber":"",
                    "role":""
              }
    except JWTError as e:
        return{
                    "status" : 0,
                    "message":f"Invalid token: {e}",
                    "mobilenumber":"",
                    "role":""
              }
#check if the user is an admin:
def require_admin(user : dict = Depends(get_current_user)):
    if user['role']=="":
        return user
    if user['role']!="admin":
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
        data={"sub": verificationStatus['db_user'].mobileNumber, "role": verificationStatus['db_user'].role}, expires_delta=access_token_expires)
    return {"status":"1", "message":"login successfully","isCustomer":verificationStatus['isCustomer'],"access_token": access_token, "token_type": "bearer"}

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
            db_user =ClientRegistrationModel(**post)
            db.add(db_user) 
            db.commit()
            db.refresh(db_user)
            jsonRegistrationstatus={"status":1,"message":"Resgistration done successfully"}
        except Exception as e:
            jsonRegistrationstatus = {"status":"0", "message":f" Error: {e}"}
    return jsonRegistrationstatus

@app.post("/amountDisplay")
async def amount_display(post : AmountCalc, user:dict = Depends(require_admin), db:Session = Depends(get_db2) ):
        post = post.dict()
        type_sale_purchase = post['type']
        time_period = post['period']
        print("hello1")
        amountDisplayStatus = await displayAmount_check(type_sale_purchase, time_period, db)
        return amountDisplayStatus

@app.post("/dashboard")
async def dashboard_display(post : ClientDataDashboard,db2:Session = Depends(get_db2),user : dict = Depends(require_admin)):
    #post = post.dict()
    #userid=int(post['userId'])
    #token=post['token']
    if user['status'] == 0:
        return user
    elif user['role'] == "admin":
        return await dashboard_display_admin(db2)
    else:
        return await dashboard_display_nonadmin(db2)

@app.post("/searchQuery")
async def search_query_invoice(post:ClientDataSearchQuery,db2:Session = Depends(get_db2),user : dict = Depends(require_admin)):
    if user['status'] == 0:
        return user
    
    post_dic= post.dict()
    sType = post_dic['sType']
    typeFilter  =  post_dic["typeFilter"]
    flag = int(post_dic['flag'])
     
    if flag == 0:
        return(await party_list_search_query(post,db2))
    elif(flag == 1):
        if typeFilter == "invoice":
            return(await search_query_invoice_func(post,db2))
        elif typeFilter == "party":
            return(await search_query_party_func(post,db2))
        elif typeFilter == "date":
            return(await search_query_date_func(post,db2))
    
    


