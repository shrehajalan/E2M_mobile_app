from sqlalchemy.orm import Session
from schema_data import EmployeeRegistration
from models import EmployeeRegistrationModel, ClientRegistrationModel, EmployeeJobDetailsModel,EmployeeOtpModel
from models import EmployeeSalaryPaymentModel,EmployeeExtraPaymentModel,ExpenseModel,EmployeeAttendanceModel
import string
import smtplib
import random
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from math import radians, sin, cos, sqrt, atan2
import calendar
from sqlalchemy import extract

async def check_employee_registration(latitude : str, longitude : str, post1 : dict, post2 : dict, db3 : Session):
    try:
        lat_str = latitude
        long_str = longitude
        
        if lat_str[-1] not in ['N', 'S']:
            raise ValueError(f"Invalid latitude format: {lat_str}")
        if long_str[-1] not in ['E', 'W']:
            raise ValueError(f"Invalid longitude format: {long_str}")
        
        post = post1.copy()
        post['empReportingLatitude'] = float(lat_str[:-1]) if lat_str[-1] =='N' else -float(lat_str[:-1])
        post['empReportingLongitude'] = float(long_str[:-1])  if long_str[-1] == 'E' else -float(long_str[:-1])
        post['role'] = 'nonadmin'
        db3_user = EmployeeRegistrationModel(**post)
        db3.add(db3_user) 
        db3.commit()
        db3.refresh(db3_user)

        db3_user_job_details = EmployeeJobDetailsModel(**post2)
        db3.add(db3_user_job_details) 
        db3.commit()
        db3.refresh(db3_user_job_details)
        jsonRegistrationstatus={"status":1,"message":"Employee registration done successfully"}

    except ValueError as ve:
    # Custom ValueError message for format issues
        jsonRegistrationstatus = {"status": 0, "message": f"Invalid coordinate format: {ve}"}

    except Exception as e:
        jsonRegistrationstatus = {"status":"0", "message":f" Error: {e}"}

    return(jsonRegistrationstatus)

async def generate_unique_employee_code(clientId : string, mob:string, db : Session, db3 : Session):
    record = db.query(ClientRegistrationModel).filter_by(clientId = clientId).first()
    unique_code = record.uniqueCode
    return(unique_code)

    #any_records = db3.query(EmployeeRegistrationModel).order_by(EmployeeRegistrationModel.employeeId.desc()).first()
    #empNo = any_records.employeeId + 1 if any_records else 1

    #employee_unique_num = unique_code + str(empNo)
    #print("EMPL_UC",employee_unique_num)

async def check_new_employee_mob(mob:string, db3 : Session):
    empId = db3.query(EmployeeRegistrationModel.employeeId).filter(EmployeeRegistrationModel.mobileNum==mob).first()
    dic={}
    if empId == None:
        dic={'status':0,'empID':None}
        return dic
    else :
        dic={'status':1,'empId':empId}
    return dic

async def check_unique_values(accnum : str, proofnum : str, upiid : str, mailId : str, db3 : Session):
    existing_record = db3.query(EmployeeRegistrationModel).filter(
    (EmployeeRegistrationModel.accountNumber == accnum) |
    (EmployeeRegistrationModel.proofNumber == proofnum) |
    (EmployeeRegistrationModel.mailId == mailId)|
    (EmployeeRegistrationModel.upiId == upiid)).all()

    dic={}
    if existing_record == []: 
        dic={'status':0}
    else :
        dic={'status':1}
    return dic

async def extract_client_code(empId : str, db : Session) :
    client_code = empId[:4]
    clientId = db.query(ClientRegistrationModel.clientId).filter(ClientRegistrationModel.uniqueCode == client_code).scalar()
    if clientId == None:
        return({'status':0,'message':"entered wrong empid",'clientId': "",'empId':"",'access_token':"","token_type":""})
    else:
        return({'status':1, 'message':"successfully extrcated the client id", 'clientId': clientId})

async def emp_login_verification(post : dict, db3 : Session):
    empId = post['empId'][4:]
    record = db3.query(EmployeeRegistrationModel).filter(EmployeeRegistrationModel.employeeId == empId).first() 
    if record is None:
        return({'status':0, 'message':"entered wrong empId"})
    else:
        if(record.password == post['password']):
            return({'status':1, 'message':" successful login", "data" : record })
        else:
            return({'status':0, 'message':"entered wrong password"})
        
async def emp_record_verification(empId : str, db3 : Session):
    employeeNum = int(empId[4:])
    record = db3.query(EmployeeRegistrationModel).filter(EmployeeRegistrationModel.employeeId == employeeNum).first() 
    if record is None:
        return({'status': 0, 'message':"entered wrong empId",'clientId':"", "employeeNum":""})
    else:
         return({'status':1, 'message':"verified empId ",'clientId':"", "employeeNum":employeeNum})

async def emp_generate_otp(empId : int, db3 : Session):
    otp = str(random.randint(100000, 999999))
    post1 = {'employeeId':empId,"otp":otp }
    db3_emp_otp =EmployeeOtpModel(**post1)
    db3.add(db3_emp_otp ) 
    db3.commit()
    db3.refresh(db3_emp_otp )
    #receiver_mail = db3.query(EmployeeRegistrationModel.mailId).filter(EmployeeRegistrationModel.employeeId == empId).scalar()
    receiver_mail = "shrehajalan1812@gmail.com"
    sender_email = "shrehajalan2808@gmail.com"
    sender_password = "mosu uhok rscq cwst"
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_mail
    message["Subject"] = "Your OTP Code"

    body = f"Your OTP for password reset is: {otp}"
    message.attach(MIMEText(body, "plain"))
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_mail, message.as_string())
        server.quit()
        return({'status':1, 'message':"otp sent to registered mailId",'clientId':"", "employeeNum":empId})
        
    except Exception as e:
        return({'status':0, "message":f'error: {e}','clientId':"", "employeeNum":""})
   
async def emp_otp_check(employeeNum : str, otp : str, db3 : Session):
    otp_record = db3.query(EmployeeOtpModel).filter(EmployeeOtpModel.employeeId == employeeNum).first()
    if otp_record.otp == otp:
        db3.delete(otp_record)  # Delete the record
        db3.commit() 
        return({'status':1,'message':"otp matched",'clientId':"", "employeeNum":employeeNum})
    else:
        db3.delete(otp_record)  # Delete the record
        db3.commit() 
        return({'status':0,'message':"otp did not match",'clientId':"", "employeeNum":employeeNum})
    
async def emp_password_change(employeeNum : str, newPassword : str, db3 : Session):
    record = db3.query(EmployeeRegistrationModel).filter(EmployeeRegistrationModel.employeeId == employeeNum).first() 
    if record:
        record.password = newPassword 
        db3.commit()
        return({'status':1,'message':"password updated successfully", "employeeNum":employeeNum})
    else:
        return({'status':0,'message':"employee not found", "employeeNum":employeeNum})

async def emp_name_list(post : dict, db3: Session):
    try:
       records_per_page = 10
       searchWord = post['empName']
       pageNum  = int(post['pageNum'])
       totalPages = int(post['totalPages'])

       baseQuery =  db3.query(EmployeeRegistrationModel).filter(EmployeeRegistrationModel.name.contains(searchWord))
       if pageNum == -1 : 
           total_records = baseQuery.count()
           records = baseQuery.limit(records_per_page).all()
           total_pages = (total_records + records_per_page - 1) // records_per_page
           if not(records):
                total_pages = -1
                page_num = -1
                message = "successful search with 0 matching employee name"
           else:
                page_num = 1 
                message = "successful search"
           return{"status": 1,"message": message,"records":[{"employeeName":row.name,"employeeNum":row.employeeId} for row in records],"page_num": page_num,"total_pages": total_pages}
       else:
           page_num = pageNum
           offset = (pageNum - 1) * records_per_page
           records = baseQuery.offset(offset).limit(records_per_page).all()
           return{"status": 1,"message":"successful search","records":[{"employeeName":row.name,"employeeNum":row.employeeId} for row in records],"page_num": page_num,"total_pages": totalPages}   
    except Exception as e:
        return({"status": 0,"message":f"Error: {e}","records":[],"page_num":"","total_pages":""})

async def emp_salary_entry(post : dict, db3 : Session):
    try: 
        if post['flag'] == '0':

            estimated_salary_status = await emp_estimated_salary(post,db3)
            return(estimated_salary_status)
        
        elif post['flag'] == '1':
            post1 = {}
            post1['employeeId'] = int(post['employeeNum'])
            post1["salaryMonth"] = post["salaryMonth"]
            post1["salaryYear"] = post["salaryYear"]
            post1["paymentDate"] = datetime.strptime(post['paymentDate'], "%Y-%m-%d").date() 
            post1["paymentMode"] = post["paymentMode"]
            post1["description"] = post["description"]
            post1["amountPaid"] = float(post["amountPaid"])

            leavesCarriedForward = post['nextMonthLeavesCarriedForward']
            emp_record = db3.query(EmployeeJobDetailsModel).filter(EmployeeJobDetailsModel.employeeId == int(post['employeeNum'])).first()
            emp_record.leavesCarriedForward = leavesCarriedForward
            db3.commit()  
            db3.refresh(emp_record) 

            db3_emp_sal_record = EmployeeSalaryPaymentModel(**post1)
            db3.add(db3_emp_sal_record) 
            db3.commit()
            db3.refresh(db3_emp_sal_record)
            status = {"status":1,"message":"salary added to the system successfully"}

    except Exception as e:
        status = {"status":"0", "message":f" Error: {e}"}
    return status

async def emp_estimated_salary(post : dict, db3 : Session):
    employeeNum = post['employeeNum']
    salaryMonth = post['salaryMonth']
    salaryYear = int(post['salaryYear'])
    salaryMonthNum = list(calendar.month_name).index(salaryMonth)

    record1 = db3.query(EmployeeJobDetailsModel).filter(EmployeeJobDetailsModel.employeeId == employeeNum).first()
    joinMonthNum = record1.joinDate.month
    joinYear = record1.joinDate.year
    if salaryYear <= joinYear and salaryMonthNum < joinMonthNum:
            return({"status":1,"message":f"No salary paid for the month {salaryMonth} as the employee was not registered with the organisation"})

    currentMonthNum = datetime.now().month
    currentYear = datetime.now().year
    if salaryYear >= currentYear and  salaryMonthNum > currentMonthNum:
        return({"status":1,"message":"Salary cannot be entered for a future month."})
               
    record = db3.query(EmployeeSalaryPaymentModel).filter(EmployeeSalaryPaymentModel.employeeId == employeeNum).order_by(EmployeeSalaryPaymentModel.paymentDate.desc()).first()
    
    if not record:
        month_diff = 1
    else:
        lastPaidSalaryMonthNum = list(calendar.month_name).index(record.salaryMonth)
        lastPaidSalaryYear = int(record.salaryYear)

        if lastPaidSalaryYear != salaryYear:
            month_diff = (12 - lastPaidSalaryMonthNum) + salaryMonthNum
        else:
            month_diff = salaryMonthNum - lastPaidSalaryMonthNum
     
    if month_diff <= 0:
        status = {"status":1,"message":"salary is already paid"}
    elif month_diff == 1:
        currentMonthNum = datetime.now().month

        if currentMonthNum == salaryMonthNum:
            flag_month_diff = 0
            estimated_value = await salary_estimate_calc(post,db3,flag_month_diff)
            status = {"status":1,"message":"salary is estimated till date , but can proceed with salary payment next month","data":[estimated_value]}
        else:
            flag_month_diff = 1
            estimated_value = await salary_estimate_calc(post,db3,flag_month_diff)
            status = {"status":1,"message":"salary is estimated for entire month and can proceed to pay salary","data":[estimated_value]}
    else:
        status = {"status":1,"message":f"salary was last paid for {record.salaryMonth} {lastPaidSalaryYear}.Please proceed to pay for {calendar.month_name[lastPaidSalaryMonthNum]} {lastPaidSalaryYear}"}
    return status

async def salary_estimate_calc(post : dict, db3 : Session, flag_month_diff : int):
    employeeNum = int(post['employeeNum'])
    salaryMonth = post['salaryMonth']
    salaryYear = int(post['salaryYear'])
    salaryMonthNum = list(calendar.month_name).index(salaryMonth)

    emp_details_record = db3.query(EmployeeJobDetailsModel).filter(EmployeeJobDetailsModel.employeeId == employeeNum).first()
    
    emp_salary = emp_details_record.salary
    emp_leavesPerMonth = emp_details_record.leavesPerMonth
    emp_leavesCarriedForward = emp_details_record.leavesCarriedForward 

    days_of_month = calendar.monthrange(salaryYear, salaryMonthNum)[1]
    per_day_wage = emp_salary/days_of_month
    
    count_of_days_present = db3.query(EmployeeAttendanceModel).filter(EmployeeAttendanceModel.employeeId == employeeNum,
                                                 extract('month', EmployeeAttendanceModel.attendanceDate) == salaryMonthNum,
                                                 extract('year', EmployeeAttendanceModel.attendanceDate) == salaryYear                   
                                                ).count()

    if flag_month_diff == 0:
        today = datetime.today()
        start_of_month = datetime(salaryYear, salaryMonthNum, 1)
        days_count = (today - start_of_month).days + 1
        num_of_leaves_taken = days_count - count_of_days_present
    else:
        num_of_leaves_taken = days_of_month - count_of_days_present

    emp_can_avail_total_leaves = emp_leavesPerMonth + emp_leavesCarriedForward
    diff = emp_can_avail_total_leaves -  num_of_leaves_taken

    if diff >= 0:
        if flag_month_diff == 0:
            estimated_salary = per_day_wage * days_count
            nextMonthLeavesCarriedForward = diff
        else:
            estimated_salary =  per_day_wage * days_of_month
            nextMonthLeavesCarriedForward = 0
        return({ "salaryEstimatedFor": salaryMonth,
                 "estimatedSalary": estimated_salary,
                 "num_of leaves_can_avail_for_this_month" : emp_can_avail_total_leaves, 
                 "num_of_leaves_taken_till_date" : num_of_leaves_taken,
                 "nextMonthLeavesCarriedForward":nextMonthLeavesCarriedForward})

    else:
        estimated_salary = per_day_wage * (count_of_days_present + emp_can_avail_total_leaves)
        nextMonthLeavesCarriedForward = 0
        return({ "salaryEstimatedFor": salaryMonth,
                 "estimatedSalary": estimated_salary,
                 "num_of leaves_can_avail_for_this_month" : emp_can_avail_total_leaves,
                 "num_of_leaves_taken_till_date" : num_of_leaves_taken,
                 "nextMonthLeavesCarriedForward":nextMonthLeavesCarriedForward})

    
    
async def emp_extra_payment_entry(post : dict, db3 : Session):
    try:
        post["amount"] = float(post["amount"]) 
        payment_type = post['paymentType']
        employeeNum = post['employeeNum']

        if payment_type == "Advance Given":
            record = db3.query(EmployeeJobDetailsModel).filter(EmployeeJobDetailsModel.employeeId == employeeNum).first()
            if record: 
                record.totalAdvance += post['amount']
                db3.commit() 
                status = {"status":1, "message" : "advance given updated successfully"}
            else:
                status = {"status":0, "message" : "employee not found"}

        if payment_type == "Advance Returned":
            record = db3.query(EmployeeJobDetailsModel).filter(EmployeeJobDetailsModel.employeeId == employeeNum).first()
            if record: 
                record.totalAdvance -= post['amount']
                db3.commit() 
            else:
                status = {"status":0, "message" : "employee not found"}
        
        post1 = post 
        del(post1['clientId'])
        del(post1['empName'])
        post1['employeeId'] = post['employeeNum']
        del(post1['employeeNum'])
        
        db3_emp_extra_payment_record = EmployeeExtraPaymentModel(**post1)
        db3.add(db3_emp_extra_payment_record) 
        db3.commit()
        db3.refresh(db3_emp_extra_payment_record)
        status = {"status":1,"message":"extra payment/adjustment added to the system successfully"}
    except Exception as e:
        status = {"status":"0", "message":f" Error: {e}"}
    return status

async def expense_entry(post : dict, db3 : Session):
    try:
        post["amount"] = float(post["amount"]) 
        del(post['clientId'])

        db3_expense_record = ExpenseModel(**post)
        db3.add(db3_expense_record) 
        db3.commit()
        db3.refresh(db3_expense_record)
        status = {"status":1,"message":"expense added successfully"}
    except Exception as e:
        status = {"status":"0", "message":f" Error: {e}"}
    return status

async def emp_mark_attendance(post : dict, db3 : Session):
 try:
    employeeNum = int(post['employeeNum'])
    date = post['attendanceDate']
    record = db3.query(EmployeeAttendanceModel).filter(EmployeeAttendanceModel.employeeId == employeeNum, EmployeeAttendanceModel.attendanceDate == date).first()
    if record : 
       return{'status':0,'message':"Employees attendance is already marked.No multiple times attendance are allowed"} 
    record = db3.query(EmployeeRegistrationModel).filter(EmployeeRegistrationModel.employeeId == employeeNum).first()
    emp_name = record.name
    shop_long = record.empReportingLongitude 
    shop_lat = record.empReportingLatitude
    curr_long = float(post['curLongitude'][:-1]) if "E" in post['curLongitude'] else -float(post['curLongitude'][:-1])
    curr_lat = float(post['curLatitude'][:-1]) if "N" in post['curLatitude'] else -float(post['curLatitude'][:-1])

    allowed_radius = 100
    R = 6371000
    shop_long, shop_lat, curr_long, curr_lat = map(radians, [shop_long, shop_lat, curr_long, curr_lat])

    dlat = shop_lat - curr_lat
    dlon = shop_long - curr_long

    # Apply Haversine formula
    a = sin(dlat/2)**2 + cos(shop_lat) * cos(shop_long) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c  # Distance in meters
    if distance <= allowed_radius:
        attendance_mark = 1
        attendance_status = {'status':1,'message':"Employee is within the allowed radius.Attendance marked successfully."}
    else:
        attendance_mark = 0
        attendance_status = {'status':0,'message':"Employee is not within the allowed radius."}
    post1 = post
    del(post1["clientId"])
    del(post1["empPresentStatus"])
    post1['empPresentStatus']  = attendance_mark
    post1['curLatitude'] = curr_lat
    post1['curLongitude'] = curr_long

    if attendance_status['status'] == 1:
        emp_attendance = EmployeeAttendanceModel(**post)
        db3.add(emp_attendance)
        db3.commit()
        db3.refresh(emp_attendance)
    elif attendance_status['status'] == 0:
        receiver_mail = "shrehajalan1812@gmail.com"
        sender_email = "shrehajalan2808@gmail.com"
        sender_password = "mosu uhok rscq cwst"
    
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_mail
        message["Subject"] = f"Employee Number : {employeeNum} is trying to mark attendance out of range"

        body = f"Employee with Employee Number : {employeeNum} and Employee Name : {emp_name} is trying to mark attendance outside the allowed range"
        message.attach(MIMEText(body, "plain"))
    
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_mail, message.as_string())
        server.quit()
        return({'status':0,'message':"Employee is not within the allowed radius. Attendance cannot be marked present.Mail to sent to admin"})
    return(attendance_status)
 
 except Exception as e:
        return({'status':0, "message":f'error: {e}'})










